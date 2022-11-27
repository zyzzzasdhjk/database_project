import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLabel, QItemDelegate, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, \
    QTableView
from PyQt5 import QtWidgets, QtCore, QtGui
from gui import AddMenu

mid = 0
sheet_lst = []


class MyButtonDelegate(QItemDelegate):
    """创建按钮代理"""

    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('+'),
                self.parent(),
                clicked=self.parent().addM
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
    addMenuSignal = pyqtSignal(int, int)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')
        self.lst = lst
        # 路径列表
        self.setPlaylistTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(1, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的六项属性二维列表"""
        self.model = QStandardItemModel(0, 0)
        self.Headers = ['歌单', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            item = QStandardItem(f'{lst[row][1]}')
            self.model.setItem(row, 0, item)

    def setPlaylistTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def addM(self):
        """播放按钮的信号
            发出：歌曲路径"""
        print(mid, self.lst[self.sender().index][0])
        self.addMenuSignal.emit(mid, self.lst[self.sender().index][0])


class add_menu(QtWidgets.QWidget, AddMenu.Ui_Form):  # 修改main_ui.Ui_MainWindow

    def __init__(self):
        super(add_menu, self).__init__()
        self.setupUi(self)
        self.ini()

    def ini(self):
        pass

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
        self.table.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.table_list.addWidget(self.table)

    def getMid(self, n):
        global mid
        mid = n

    def getSheet(self, lst):
        global sheet_lst
        sheet_lst = lst
# select * from (select MID,count(*) n from SID_MID group by MID) as A left join Music as M on A.MID=M.MID order by n
# desc
