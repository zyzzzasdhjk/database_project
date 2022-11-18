import random
import threading
from PyQt5 import QtWidgets
import pygame
import sys
from lib import MyJson as js
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLabel, QWidget, QTableView, QVBoxLayout
from mutagen.mp3 import MP3

from gui import main_ui, music_ui  # 导入ui文件

thread_flag1 = 0  # 进度条线程暂停的标志
time_change = 0  # 由于pygame库的模块只能获取已播放的时长，故增加
music_time_change_flag = 0  # 进度条被修改的标志
pygame.mixer.init()  # 初始化混音器模块（pygame库的通用做法，每一个模块在使用时都要初始化pygame.init()为初始化所有的pygame模块，可以使用它也可以单初始化这一个模块）


def num_format(n):  # 将两位数及以下的数字转化为两位数的字符串
    return '0{}'.format(n) if 0 <= n < 10 else "{}".format(n)


def time_format(t):  # 获取一个以秒单位的时长，转化为**:**:**的格式
    s = t % 60
    m = t % 3600 // 60
    h = t // 3600
    return f"{num_format(h)}:{num_format(m)}:{num_format(s)}"


def get_music_time(filename):  # 获取音乐文件的时长，返回值是一个整数，单位为秒
    audio = MP3(filename)
    return int(audio.info.length)


def start_music(filename, time=0):
    pygame.mixer.music.load(filename)  # 加载音乐
    pygame.mixer.music.play(start=time)


def set_music_volume(x=0.5):
    pygame.mixer.music.set_volume(x)  # 设置音量大小0~1的浮点数


def set_music_time(t):  # 修改音乐播放的时间
    pygame.mixer.music.set_pos(t)
    # pygame.mixer.music.play(start=t)
    global music_time_change_flag
    music_time_change_flag = 0


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.music = Music_player()
        self.ini_window()

    def ini_window(self):
        self.bottom_layout.addWidget(self.music)
        self.music.show()


class Music_player(QtWidgets.QWidget, music_ui.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self):
        super(Music_player, self).__init__()
        self.setupUi(self)
        # 初始化变量
        self.music_last_time = 0  # 滑块拖动时的时间
        self.music_pause_flag = 0  # 1代表被暂停，刚开始应该是暂停的
        self.music_play_manner_flag = 0  # 用于控制播放方式，1为列表循环，2为单曲循环，3为随机播放
        # 初始化要用的变量
        self.creator_name = ''  # 歌手名字
        self.music_name = ""  # 歌曲名字
        self.music_time = 0  # 歌曲时间
        self.time_slider_thread = None  # 控制进度条的线程
        self.music_num = 0  # 当前音乐再列表的位置
        self.music_path = None  # 音乐路径
        self.music_lst = []  # 音乐列表
        self.music_lst_len = 0  # 音乐列表长度
        self.music_random_lst = []  # 音乐随机播放列表
        self.music_random_lst_len = 0  # 音乐随机播放列表长度
        self.thread_flag2 = False

        self.ini_window()

    def ini_window(self):
        # 读取json文件
        j = js.json_load_file("./data/music_lst.json")
        self.music_num = j[0]
        self.music_play_manner_flag = j[1]
        global time_change
        time_change = j[2]
        self.music_lst = j[3]
        set_music_volume(0)
        self.load_music()
        self.pause_music()  # 调用函数暂停音乐
        set_music_volume()
        self.music_time = get_music_time(self.music_path)
        self.time_slider_thread = threading.Thread(target=self.update_slider)
        # 初始化进度条模块
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(1000)
        self.time_slider.setSingleStep(1)
        self.right_time_label.setText(time_format(self.music_time))
        # 根据记录初始化上次的页面
        self.update_play_manner_button()
        self.update_left_label_time(flag=1)
        # 初始化控制按钮
        self.suspend_button.clicked.connect(self.pause_music)  # 绑定暂停事件
        self.play_manner_button.clicked.connect(self.play_manner)  # 绑定播放方式更改
        self.time_slider.sliderPressed.connect(self.f1)
        self.time_slider.sliderReleased.connect(self.f2)
        self.next_button.clicked.connect(self.load_next_music)
        self.previous_button.clicked.connect(self.load_previous_music)
        # 启动线程
        self.time_slider_thread.start()

    def update_left_label_time(self, flag=0):  # 更新左侧的label
        if flag == 0:
            t = self.time_slider.value()  # 注意，返回值是一个整数
            self.left_time_label.setText(time_format(int(get_music_time(self.music_name) * (t / 100.0))))
        else:
            self.left_time_label.setText(time_format(time_change))
            self.time_slider.setValue(int(time_change / self.music_time * 1000))

    def update_slider(self):  # 根据传入的时间（秒）更新进度条
        while True:
            if self.thread_flag2:
                break
            if thread_flag1:
                continue
            t = time_change + pygame.mixer.music.get_pos() / 1000
            if abs(t - self.music_time) < 0.5:
                self.load_next_music()
                continue
            self.time_slider.setValue(int(t / self.music_time * 1000))
            self.left_time_label.setText(time_format(int(t)) + " ")
            if music_time_change_flag == 1:
                set_music_time(t)

    def f1(self):  # 滑块被按下的时的操作
        self.music_last_time = self.time_slider.value()
        global thread_flag1
        thread_flag1 = 1

    def f2(self):  # 滑块被释放时的操作
        global thread_flag1, time_change, music_time_change_flag
        thread_flag1 = 0
        music_time_change_flag = 1
        time_change += (self.time_slider.value() - self.music_last_time) / 1000 * self.music_time

    def pause_music(self):  # 控制音乐播放
        global thread_flag1
        if self.music_pause_flag:
            pygame.mixer.music.unpause()
            thread_flag1 = 0
            self.suspend_button.setText("暂停")
            self.music_pause_flag = 0
        else:
            pygame.mixer.music.pause()
            thread_flag1 = 1
            self.suspend_button.setText("继续")
            self.music_pause_flag = 1

    def update_play_manner_button(self):
        if self.music_play_manner_flag == 0:
            self.play_manner_button.setText("列表循环")
        elif self.music_play_manner_flag == 1:
            self.play_manner_button.setText("单曲循环")
        elif self.music_play_manner_flag == 2:
            self.play_manner_button.setText("随机播放")

    def play_manner(self):
        if self.music_play_manner_flag == 0:
            self.music_play_manner_flag = 1
            self.update_play_manner_button()
        elif self.music_play_manner_flag == 1:
            self.music_play_manner_flag = 2
            self.update_play_manner_button()
        elif self.music_play_manner_flag == 2:
            self.music_play_manner_flag = 0
            self.update_play_manner_button()

    def load_music(self, flag=1):
        self.music_name = self.music_lst[self.music_num][0]
        self.creator_name = self.music_lst[self.music_num][1]
        self.music_path = self.music_lst[self.music_num][2]
        if flag == 0:  # 代表无音乐
            self.name_label.setText("无")
            self.creator_label.setText("无")
        else:
            self.name_label.setText(self.music_name)
            self.creator_label.setText(self.creator_name)
            self.music_time = get_music_time(self.music_path)
            start_music(self.music_path, time=time_change)

    def modify_music_num_by_music_manner(self):
        self.music_lst_len = len(self.music_lst)
        if self.music_play_manner_flag == 0:
            if self.music_num == -1:
                self.music_num = self.music_lst_len - 1
            elif self.music_num == self.music_lst_len:
                self.music_num = 0
        elif self.music_play_manner_flag == 1:
            self.music_num-=1
        else:
            self.music_num = random.randint(0, self.music_lst_len - 1)

    def load_next_music(self):
        global time_change
        self.music_num += 1
        self.modify_music_num_by_music_manner()
        time_change = 0
        self.load_music()
        self.music_pause_flag = 1
        self.pause_music()
        self.right_time_label.setText(time_format(get_music_time(self.music_path)))

    def load_previous_music(self):
        global time_change
        self.music_num -= 1
        self.modify_music_num_by_music_manner()
        time_change = 0
        self.load_music()
        self.music_pause_flag = 1
        self.pause_music()
        self.right_time_label.setText(time_format(get_music_time(self.music_path)))

    def playlist_widget(self):
        pass

    def save_json(self):
        self.thread_flag2 = 1
        js.json_write_file("./data/music_lst.json",
                           [self.music_num, self.music_play_manner_flag,
                            int(self.time_slider.value() / 1000 * self.music_time), self.music_lst])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
