import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QListWidget
import sys

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QTableWidget

import MusicPlayer
from gui import main_ui  # 导入ui文件


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.music = MusicPlayer.Music_player()
        self.ini_window()

    def ini_window(self):
        self.bottom_layout.addWidget(self.music)
        self.music.show()

    def closeEvent(self, event):
        self.music.save_json()
        print(11)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
