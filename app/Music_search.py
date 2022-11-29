from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import QLabel, QItemDelegate, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, \
    QTableView
from PyQt5 import QtWidgets, QtCore, QtGui
from gui import music_search
from mutagen.mp3 import MP3


def num_format(n):  # 将两位数及以下的数字转化为两位数的字符串
    return '0{}'.format(n) if 0 <= n < 10 else "{}".format(n)


def time_format(t):  # 获取一个以秒单位的时长，转化为**:**:**的格式
    s = t % 60
    m = t % 3600 // 60
    return f"{num_format(m)}:{num_format(s)}"


def get_music_time(filename):  # 获取音乐文件的时长，返回值是一个整数，单位为秒
    audio = MP3(filename)
    return int(audio.info.length)


class MyButtonDelegate(QItemDelegate):
    """创建按钮代理"""

    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('*'),
                self.parent(),
                clicked=self.parent().startPlay
            )
            button_next = QPushButton(
                self.tr('+'),
                self.parent(),
                clicked=self.parent().startNextPlay
            )
            button_add = QPushButton(
                self.tr('add'),
                self.parent(),
                clicked=self.parent().addMenu
            )
            button_read.index = index.row()
            button_add.index = index.row()
            button_next.index = index.row()
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_next)
            h_box_layout.addWidget(button_add)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )


class PersonButton(QItemDelegate):
    """创建按钮代理"""

    def __init__(self, parent=None):
        super(PersonButton, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('访问'),
                self.parent(),
                clicked=self.parent().emit_user_uid
            )
            button_read.index = index.row()
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )


class CLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    # 可在外部与槽函数连接
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class MyTableView(QTableView):
    """创建音乐表视图"""
    addMenuSignal = pyqtSignal(int)
    startplaysignal = pyqtSignal(list)
    startNextPlaySignal = pyqtSignal(list)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')
        self.lst = lst
        self.music_lst = [[i[1], i[2], i[-1]] for i in lst]
        # 路径列表
        self.setPlaylistTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(5, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的六项属性二维列表"""
        self.model = QStandardItemModel(0, 0)
        self.Headers = ['歌名', '歌手', '创建时间', '专辑', '时长', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            for column in range(5):
                item = QStandardItem(f'{lst[row][column + 1]}')
                self.model.setItem(row, column, item)
            self.model.setItem(row, 4, QStandardItem(time_format(get_music_time(lst[row][-1]))))

    def setPlaylistTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def startPlay(self):
        """播放按钮的信号
            发出：歌曲路径"""
        self.startplaysignal.emit(self.music_lst[self.sender().index])

    def startNextPlay(self):
        self.startNextPlaySignal.emit(self.music_lst[self.sender().index])

    def addMenu(self):
        print(self.lst[self.sender().index][0])
        self.addMenuSignal.emit(self.lst[self.sender().index][0])


class PersonTableView(QTableView):
    """创建音乐表视图"""
    visitOther = pyqtSignal(int)

    def __init__(self, parent=None, lst=None):
        super(PersonTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')
        self.lst = lst
        # 路径列表
        self.setPlaylistTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(3, PersonButton(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的六项属性二维列表"""
        self.model = QStandardItemModel(0, 0)
        self.Headers = ['用户uid', '用户名', '用户简介','操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            for column in range(3):
                item = QStandardItem(f'{lst[row][column]}')
                self.model.setItem(row, column, item)

    def setPlaylistTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def emit_user_uid(self):
        self.visitOther.emit(self.lst[self.sender().index][0])


class Search(QtWidgets.QWidget, music_search.Ui_Form):  # 修改main_ui.Ui_MainWindow
    search_type = pyqtSignal(str)
    """创建音乐表视图"""
    startplaysignal = pyqtSignal(list)
    favorThisMusicsignal = pyqtSignal(int)

    def __init__(self):
        super(Search, self).__init__()
        self.setupUi(self)
        self.music_path_lst = []
        self.search_for_music = CLabel("歌曲")
        self.search_for_music.setStyleSheet('font: 18pt "微软雅黑";')
        self.main_layout.addWidget(self.search_for_music)
        self.search_for_musician = CLabel("歌手")
        self.search_for_musician.setStyleSheet('font: 18pt "微软雅黑";')
        self.main_layout.addWidget(self.search_for_musician)
        self.search_for_playlist = CLabel("歌单")
        self.search_for_playlist.setStyleSheet('font: 18pt "微软雅黑";')
        self.main_layout.addWidget(self.search_for_playlist)
        self.search_for_person = CLabel("用户")
        self.search_for_person.setStyleSheet('font: 18pt "微软雅黑";')
        self.main_layout.addWidget(self.search_for_person)
        self.main_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,
                                                       QtWidgets.QSizePolicy.Minimum))
        self.ini()

    def ini(self):
        self.search_for_music.connect_customized_slot(self.music_type)
        self.search_for_musician.connect_customized_slot(self.musician_type)
        self.search_for_playlist.connect_customized_slot(self.playlist_type)
        self.search_for_person.connect_customized_slot(self.person_type)

    def music_type(self):
        self.search_type.emit("歌曲")

    def musician_type(self):
        self.search_type.emit("歌手")

    def playlist_type(self):
        self.search_type.emit("歌单")

    def person_type(self):
        self.search_type.emit("用户")

    def update_tableView_music(self, lst):
        """接收二位列表"""
        self.tabel = MyTableView(lst=lst)
        self.tabel_layout.addWidget(self.tabel)

    def update_tableView_person(self, lst):
        self.tabel = PersonTableView(lst=lst)
        self.tabel_layout.addWidget(self.tabel)
