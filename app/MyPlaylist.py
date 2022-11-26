from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLabel, QItemDelegate, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, \
    QTableView
from PyQt5 import QtWidgets, QtCore, QtGui
from gui import MyPlaylist
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
                self.tr('播放'),
                self.parent(),
                clicked=self.parent().startPlay
            )
            button_delete = QPushButton(
                self.tr('删除'),
                self.parent(),
                clicked=self.parent().deleteThisMusic
            )
            button_read.index = index.row()
            button_delete.index = index.row()
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_delete)
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
    update_music_lst = pyqtSignal(list)
    startplaysignal = pyqtSignal(list)
    deleteThisMusicsignal = pyqtSignal(int)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')
        self.lst = lst
        # 路径列表
        self.setPlaylistTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(3, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的六项属性二维列表"""
        self.model = QStandardItemModel(0, 0)
        self.Headers = ['歌名', '歌手', '时长', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            for column in range(2):
                item = QStandardItem(f'{lst[row][column]}')
                self.model.setItem(row, column, item)
            self.model.setItem(row, 2, QStandardItem(time_format(get_music_time(lst[row][-1]))))

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
        self.startplaysignal.emit(self.lst[self.sender().index])

    def deleteThisMusic(self):
        """收藏按钮的信号
            发出：MID"""
        self.deleteThisMusicsignal.emit(self.sender().index)
        self.parent().repaint_t()

    def emit_music_lst(self):  # 传出一个列表，[数字（0：增加，1：删除），列表（增加或删除的值）]
        """删除当前歌曲"""
        pass


class My_playlist(QtWidgets.QWidget, MyPlaylist.Ui_Form):  # 修改main_ui.Ui_MainWindow

    def __init__(self):
        super(My_playlist, self).__init__()
        self.setupUi(self)
        self.music_lst = []
        self.ini()

    def ini(self):
        pass

    def music_type(self):
        self.search_type.emit("歌曲")

    def musician_type(self):
        self.search_type.emit("歌手")

    def playlist_type(self):
        self.search_type.emit("歌单")

    def person_type(self):
        self.search_type.emit("用户")

    def repaint_t(self):
        # self.music_lst.pop
        self.update_tableView_music(self.music_lst)

    def update_tableView_music(self, lst):
        """接收二位列表"""
        self.music_lst = lst
        deleted = self.table_list.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        self.tabel = MyTableView(lst=lst)
        self.table_list.addWidget(self.tabel)
