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
                self.tr('收藏'),
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
        self.music_lst = [[i[1],i[2],i[-1]] for i in lst]
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
                item = QStandardItem(f'{lst[row][column+1]}')
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


class Music_r(QtWidgets.QWidget, MyPlaylist.Ui_Form):  # 修改main_ui.Ui_MainWindow

    def __init__(self):
        super(Music_r, self).__init__()
        self.setupUi(self)
        self.music_lst = []
        self.ini()

    def ini(self):
        self.label.setText("歌曲推荐")

    def repaint_t(self):
        # self.music_lst.pop
        self.update_tableView_music(self.music_lst)

    def update_tableView_music(self, lst):
        """接收二位列表"""
        self.music_lst = lst
        deleted = self.table_list.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        self.table = MyTableView(lst=lst)
        self.table.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.table_list.addWidget(self.table)

# select * from (select MID,count(*) n from SID_MID group by MID) as A left join Music as M on A.MID=M.MID order by n
# desc
