from PyQt5.Qt import *
from gui.OtherShow import Ui_OtherShow
import datetime


class MyButtonDelegate(QItemDelegate):
    """创建按钮代理"""

    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('进入'),
                self.parent(),
                clicked=self.parent().enterSheet
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
    enterSheetsignal = pyqtSignal(int)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')

        self.setOtherShowTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(3, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌单的三项属性二维列表
            [[SID,SName,MusicNum]]"""

        self.model = QStandardItemModel(0, 0)
        self.Headers = ['ID', '歌单名', '歌曲数目', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            for column in range(3):
                item = QStandardItem(f'{lst[row][column]}')
                self.model.setItem(row, column, item)

    def setOtherShowTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def enterSheet(self):
        """进入按钮的信号
            发出：SID"""
        index = self.model.index(self.sender().index, 0)
        data = int(self.model.data(index))
        print(data)
        self.enterSheetsignal.emit(data)


class OtherShowPanel(QWidget, Ui_OtherShow):

    def __init__(self, parent=None, lst=[]):
        super().__init__(parent)
        self.setupUi(self)
        self.setOtherShowTableView(lst)

    def loadOtherInfo(self, lst):
        """加载个人数据
            传入个人信息数据列表
            [UID, UName, USex, UIntro, UBirthday, UIsVip, LText]"""
        self.ID = lst[0]
        self.OtherShowUNameLabel.setText(lst[1])
        if lst[2] == '1':
            self.OtherShowUSexLabel.setText("男")
        else:
            self.OtherShowUSexLabel.setText("女")
        self.OtherShowUIntroLabel.setPlainText(lst[3])
        Birthday = str(lst[4].year) + '-' + str(lst[4].month) + '-' + str(lst[4].day)
        self.OtherShowUBirthdayLabel.setText(Birthday)
        if lst[5] == '1':
            self.OtherShowUIsVIPLabel.setText(lst[5])
        self.OtherShowULabelLabel.setText(lst[6])

    def setOtherShowTableView(self, lst):
        self.OtherShowTableView = MyTableView(lst=lst)
        self.OtherShowDownLayout.addWidget(self.OtherShowTableView)

    def loadOtherShowTableViewModel(self, lst):
        """接收二维列表
        [[SID,SName,MusicNum]]"""
        self.OtherShowTableView.setOtherShowTableView(lst)


if __name__ == '__main__':
    import sys
    import qdarkstyle

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = OtherShowPanel(lst=[[1, 1, 1]])
    window.show()
    sys.exit(app.exec_())
