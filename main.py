import threading
from PyQt5 import QtWidgets
import sys
import MusicPlayer
from gui import main_ui  # 导入ui文件


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.music = MusicPlayer.Music_player()
        self.ini_window()

    def ini_window(self):
        self.main_layout.addWidget(self.music)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
