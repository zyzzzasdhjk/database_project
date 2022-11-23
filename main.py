from PyQt5 import QtWidgets
import sys
from sql import sql
from app import MusicPlayer, Sidebar, playlist_widget, PlayList_Panel, Title_block_widget, user_info_widget
from gui import main_ui  # 导入ui文件
from login_and_register.login_register_Panel import LoginRegisterPanel
global MainProgress

uid_int = 1  # 得到的uid，待完善


def loginControl(UID):  # 登录函数
    global uid_int

    uid_int = UID
    MainProgress.mainwindow = Main_window()
    MainProgress.mainwindow.show()
    MainProgress.loginregisterPanel.hide()
    print(UID)


class MainProgress(QtWidgets.QWidget):
    """主进程，包含MainWindow和LoginRegisterPanel
        当登陆成功时，UID才被赋值，MainWindow才被初始化
        由于单开进程会被取消，所以采用主进程的方式"""

    def __init__(self):
        super().__init__()

        self.loginregisterPanel = LoginRegisterPanel()
        self.mainwindow = 0


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        # 初始化数据库连接
        self.db = sql.DataBase("127.0.0.1", "sa", "5151", "MMS")
        self.music = MusicPlayer.Music_player()
        self.playlist = PlayList_Panel.PlayListPanel()
        self.sidebar = Sidebar.Sidebar_widget()
        self.playlist_widget = playlist_widget.win()
        self.title_block = Title_block_widget.title_widget()
        self.user_info = user_info_widget.User_info()
        self.music_recommend_widget = PlayList_Panel.PlayListPanel()
        # self.right_widget_lst = [self.user_info,self.music_recommend_widget,]o`
        self.ini_window()

    def ini_window(self):
        self.bottom_layout.addWidget(self.music)

        # 加载右边栏所有widget
        self.right_panel = [self.playlist, self.playlist_widget, self.user_info]
        for i in range(len(self.right_panel)):
            self.right_layout.addWidget(self.right_panel[i])
            self.right_panel[i].setVisible(False)

        self.left_layout.addWidget(self.sidebar)
        self.sidebar.widget_change_signal.connect(self.change_widget_by_signal)  # 侧边栏页面切换
        self.title_block.user_uid.connect(self.update_user_info)  # 提高个人信息
        self.title_block.widget_change_signal.connect(self.change_widget_by_signal)  # 切换到个人信息界面
        self.user_info.user_info_change.connect(self.update_user_info_db)
        '''
        注意接口
        '''
        self.playlist.PlaylistMusicListTableView.startplaysignal.connect(
            self.music.add_music_to_lst)  # 传入数组的要求 [歌曲名字，歌手名字，歌曲路径] 要求全为字符串
        self.top_layout.addWidget(self.title_block)

        # 更新歌单列表
        self.updatePlaylistInfo(1)

    def updatePlaylistInfo(self, SID):
        """更新歌单界面
            传入SID"""
        self.playlist.loadPlaylistTableViewModel(self.db.getPlaylistMusicData(1))
        self.playlist.loadPlaylistData(self.db.getPlaylistSheetData(1))

    def update_user_info(self, x):  # 传入个人信息以加载
        self.user_info.ini_combox(self.db.get_all_user_label())  # 先初始化combox
        self.user_info.ini_user_info(self.db.get_user_info(x))  # 传入列表以加载

    def update_user_info_db(self, lst):
        self.db.update_user_info(lst)
        self.user_info.ini_user_info(self.db.get_user_info(lst[0][0]))

    def closeEvent(self, event):
        self.music.save_json()

    def change_widget_by_signal(self, x):
        # 隐藏原有布局中的widget
        for i in range(len(self.right_panel)):
            # 获取布局中所有widget
            deleted = self.right_layout.itemAt(i).widget()
            deleted.setVisible(False)
            # print(deleted)
        if x == -1:
            self.user_info.setVisible(True)
        elif x == 2:
            self.playlist_widget.setVisible(True)
        elif x == 3:
            self.playlist.setVisible(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import qt_material

    # setup stylesheet
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')

    # 启动主进程
    MainProgress = MainProgress()
    MainProgress.loginregisterPanel.show()
    MainProgress.loginregisterPanel.loginPanel.checkLoginSuccesssignal.connect(loginControl)

    sys.exit(app.exec_())
