from PyQt5.Qt import *
from gui.getUserSearch import Ui_getUserSearch
import datetime


class MyButtonDelegate(QItemDelegate):
    """创建按钮代理"""

    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('查看'),
                self.parent(),
                clicked=self.parent().enterUser
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


class MyTableView(QTableView):
    """创建音乐表视图"""
    enterUsersignal = pyqtSignal(int)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')

        self.setUserSearchTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(3, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """接受一个二维列表
        [[UID, UName, USex]]"""
        self.model = QStandardItemModel(0, 0)
        self.Headers = ['ID', '昵称', '性别', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        columnNum = 3
        for row in range(rowNum):
            for column in range(columnNum):
                item = QStandardItem(str(lst[row][column]))
                self.model.setItem(row, column, item)

    def setUserSearchTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def enterUser(self):
        """进入按钮的信号
            发出：UID"""
        index = self.model.index(self.sender().index, 0)
        data = int(self.model.data(index))
        print(data)
        self.enterUsersignal.emit(data)


class getUserSearchPanel(QWidget, Ui_getUserSearch):

    def __init__(self, parent=None, lst=[]):
        super().__init__(parent)
        self.setupUi(self)
        self.setUserSearchTableView(lst)

    def setUserSearchTableView(self, lst):
        self.getUserSearchTableView = MyTableView(lst=lst)
        self.getUserSearchDownLayout.addWidget(self.getUserSearchTableView)

    def loadUserSearchTableViewModel(self, lst):
        """接收二维列表
        [[UID, UName, USex]]"""
        self.getUserSearchTableView.setUserSearchTableView(lst)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    import qt_material

    # setup stylesheet
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')
    window = getUserSearchPanel(lst=[[1, '红茶honer', '男']])
    window.show()
    sys.exit(app.exec_())
