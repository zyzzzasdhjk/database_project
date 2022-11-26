from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from gui import sidebar_ui


class Sidebar_widget(QtWidgets.QWidget, sidebar_ui.Ui_Form):  # 修改main_ui.Ui_MainWindow
    widget_change_signal = pyqtSignal(int)
    createSheetShowSignal = pyqtSignal(int)
    favorSheetShowSignal = pyqtSignal(int)
    createSheetSignal = pyqtSignal()

    def __init__(self):
        super(Sidebar_widget, self).__init__()
        self.setupUi(self)
        # 定义label
        self.ini()

    def iniCreateSheet(self, lst):
        """接受用户创建的歌单列表
            二维列表
            [[SID, SName]]"""
        while self.CreateSheetListWidget.takeItem(0):
            pass
        if lst:
            for Sheet in lst:
                self.CreateSheetListWidget.addItem(Sheet[1])

    def iniFavorSheet(self, lst):
        """接受用户收藏的歌单列表
            二维列表
            [[SID, SName]]"""
        while self.FavorSheetListWidget.takeItem(0):
            pass
        if lst:
            for Sheet in lst:
                self.FavorSheetListWidget.addItem(Sheet[1])

    def ini(self):
        self.NomalListWidget.setStyleSheet('font: 12pt "微软雅黑";')
        self.CreateSheetListWidget.setStyleSheet('font: 10pt "微软雅黑";')
        self.FavorSheetListWidget.setStyleSheet('font: 10pt "微软雅黑";')
        self.NomalListWidget.addItem("歌曲推荐")
        self.NomalListWidget.addItem("歌单推荐")
        self.NomalListWidget.addItem("搜索界面")
        self.NomalListWidget.addItem("播放列表")
        self.NomalListWidget.clicked.connect(lambda item: self.showNormalWidget(item.row()))
        self.CreateSheetListWidget.clicked.connect(lambda item: self.showCreateSheet(item.row()))
        self.FavorSheetListWidget.clicked.connect(lambda item: self.showFavorSheet(item.row()))
        self.pushButton_2.clicked.connect(lambda: self.createSheetSignal.emit())

    def showNormalWidget(self, Index):
        print(Index)
        self.widget_change_signal.emit(Index)

    def showCreateSheet(self, Index):
        self.createSheetShowSignal.emit(Index)

    def showFavorSheet(self, Index):
        self.favorSheetShowSignal.emit(Index)

