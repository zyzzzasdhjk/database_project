from gui.getMusicSearch import Ui_getMusicSearch
from PyQt5.Qt import *


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
            button_write = QPushButton(
                self.tr('收藏'),
                self.parent(),
                clicked=self.parent().favorThisMusic
            )
            button_read.index = index.row()
            button_write.index = index.row()
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_write)
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
    startplaysignal = pyqtSignal(list)
    favorThisMusicsignal = pyqtSignal(int)

    def __init__(self, parent=None, lst=None):
        super(MyTableView, self).__init__(parent)
        self.setStyleSheet('font: 10pt "微软雅黑";')
        # 路径列表
        self.music_path_lst = []
        self.setMusicSearchTableView(lst)
        # 设置按钮代理
        self.setItemDelegateForColumn(5, MyButtonDelegate(self))
        # 设置不可选中
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的六项属性二维列表"""

        self.model = QStandardItemModel(0, 0)
        self.Headers = ['ID', '歌曲名', '歌手', '时间', '专辑', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            self.music_path_lst.append([lst[row][1], lst[row][2], lst[row][5]])
            for column in range(5):
                item = QStandardItem(f'{lst[row][column]}')
                self.model.setItem(row, column, item)

    def setMusicSearchTableView(self, lst):
        self.getData(lst)
        self.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def startPlay(self):
        """播放按钮的信号
            发出：歌曲路径"""
        self.startplaysignal.emit(self.music_path_lst[self.sender().index])

    def favorThisMusic(self):
        """收藏按钮的信号
            发出：MID"""
        index = self.model.index(self.sender().index, 0)
        data = int(self.model.data(index))
        print(data)
        self.favorThisMusicsignal.emit(data)


class getMusicSearchPanel(QWidget, Ui_getMusicSearch):

    def __init__(self, parent=None, lst=[]):
        super().__init__(parent)
        self.setupUi(self)
        self.setMusicSearchTableView(lst)

    def setMusicSearchTableView(self, lst):
        self.MusicSearchTableView = MyTableView(lst=lst)
        self.getMusicSearchLayout.addWidget(self.MusicSearchTableView)

    def loadMusicSearchTableViewModel(self, lst):
        """接收二位列表"""
        self.MusicSearchTableView.setMusicSearchTableView(lst)

    def favorThisPlaylist(self):
        """收藏按钮的槽函数"""
        self.favorThisSheetsignal.emit(self.ID)


if __name__ == '__main__':
    # 0. 导入所需要的包和模块
    import sys
    import qdarkstyle

    # 1. 创建一个应用程序对象
    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # 2. 控件的操作
    # 2.1 创建控件
    window = getMusicSearchPanel(lst=[[1, 1, 1, 1, 1, 1]])
    # [[2, 2, 2, 2, 2, 2]]
    # 2.2 设置控件

    # 2.3 展示控件
    window.show()

    button = QPushButton()
    button.show()
    button.clicked.connect(lambda: window.loadMusicSearchTableViewModel([[2, 2, 2, 2, 2, 2]]))

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
