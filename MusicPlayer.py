import threading
from PyQt5 import QtWidgets
import pygame
import sys
from PyQt5.QtWidgets import QLabel, QWidget
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


def start_music(filename):
    pygame.mixer.music.load(filename)  # 加载音乐
    pygame.mixer.music.set_volume(0.5)  # 设置音量大小0~1的浮点数
    pygame.mixer.music.play(start=0)


def set_music_time(t):  # 修改音乐播放的时间
    pygame.mixer.music.play(start=t)
    global music_time_change_flag
    music_time_change_flag = 0

class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.music = Music_player()
        self.ini_window()

    def ini_window(self):
        self.main_layout.addWidget(self.music)


class Music_player(QtWidgets.QMainWindow, music_ui.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self):
        super(Music_player, self).__init__()
        self.setupUi(self)
        # 初始化变量
        self.music_last_time = 0  # 滑块拖动时的时间
        self.music_pause_flag = 0  # 1代表被暂停
        self.music_name = "./music/黄龄,关大洲 - 星河叹.mp3"
        start_music(self.music_name)
        self.music_time = get_music_time(self.music_name)
        self.time_slider_thread = threading.Thread(target=self.update_slider)
        self.ini_window()

    def ini_window(self):
        # 初始化进度条模块
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(100)
        self.time_slider.setSingleStep(1)
        self.time_slider.sliderPressed.connect(self.f1)
        self.time_slider.sliderReleased.connect(self.f2)
        self.right_time_label.setText(time_format(self.music_time) + " ")
        self.left_time_label.setText("00:00:00 ")
        # 初始化控制按钮
        self.suspend_button.clicked.connect(self.pause_music)
        # 启动线程
        self.time_slider_thread.start()


    def update_left_label_time(self):  # 更新左侧的label
        t = self.time_slider.value()  # 注意，返回值是一个整数
        self.left_time_label.setText(time_format(int(get_music_time(self.music_name) * (t / 100.0))) + " ")

    def update_slider(self):  # 根据传入的时间（秒）更新进度条
        while True:
            if thread_flag1:
                continue
            t = time_change + pygame.mixer.music.get_pos() / 1000
            self.time_slider.setValue(int(t / self.music_time * 100))
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
        time_change += (self.time_slider.value() - self.music_last_time) / 100 * self.music_time
        self.suspend_button.setText("暂停")
        self.music_pause_flag = 0

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


    def playlist_widget(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
