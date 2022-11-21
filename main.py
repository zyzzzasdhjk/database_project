from PyQt5 import QtWidgets
import sys

from app import MusicPlayer, Sidebar, playlist_widget, PlayList_Panel,Title_block_widget
from gui import main_ui  # 导入ui文件


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.music = MusicPlayer.Music_player()
        self.playlist = PlayList_Panel.PlayListPanel()
        self.sidebar = Sidebar.Sidebar_widget()
        self.playlist_widget = playlist_widget.win()
        self.title_block = Title_block_widget.title_widget()
        self.ini_window()

    def ini_window(self):
        self.bottom_layout.addWidget(self.music)
        self.right_layout.addWidget(self.playlist)
        self.left_layout.addWidget(self.sidebar)
        self.sidebar.widget_change_signal.connect(self.change_widget_by_signal)
        self.top_layout.addWidget(self.title_block)

    def closeEvent(self, event):
        self.music.save_json()

    def change_widget_by_signal(self, x):
        if x == 2:
            deleted = self.right_layout.takeAt(0)
            print(deleted)
            del deleted
            self.right_layout.addWidget(self.playlist_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import qt_material

    # setup stylesheet
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')

    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
