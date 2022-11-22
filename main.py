from PyQt5 import QtWidgets
import sys
from sql import sql
from app import MusicPlayer, Sidebar, playlist_widget, PlayList_Panel, Title_block_widget, user_info_widget
from gui import main_ui  # 导入ui文件

uid_int = 1  # 得到的uid，待完善


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
        self.sidebar.widget_change_signal.connect(self.change_widget_by_signal)
        self.title_block.user_uid.connect(self.update_user_info)
        self.title_block.widget_change_signal.connect(self.change_widget_by_signal)
        self.top_layout.addWidget(self.title_block)

    def update_user_info(self,x):
        self.user_info.ini(self.db.get_user_info(x))

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

    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
