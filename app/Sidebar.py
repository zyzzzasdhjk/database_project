from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from gui import sidebar_ui


class Sidebar_widger(QtWidgets.QWidget, sidebar_ui.Ui_Form):  # 修改main_ui.Ui_MainWindow
    widget_change_signal = pyqtSignal(int)
    def __init__(self):
        super(Sidebar_widger, self).__init__()
        self.setupUi(self)
        # 定义label
        self.playlist_lst = []
        self.load_playlist()
        self.ini()

    def load_playlist(self):
        pass

    def ini(self):
        self.listWidget.addItem("歌曲推荐")
        self.listWidget.addItem("各地推荐")
        self.listWidget.addItem("播放列表")
        self.listWidget.addItem("我的歌单")
        self.listWidget.clicked.connect(lambda item: self.change_widget(item.row()))

    def change_widget(self, x):
        print(x)
        if x == 2:
            self.widget_change_signal.emit(x)