from gui.Playlist import Ui_PlayList
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
                clicked=self.parent().cellButtonClicked
            )
            button_write = QPushButton(
                self.tr('收藏'),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            button_read.index = [index.row(), index.column()]
            button_write.index = [index.row(), index.column()]
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
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent)
        self.setItemDelegateForColumn(5, MyButtonDelegate(self))

    def cellButtonClicked(self):
        print("Cell Button Clicked", self.sender().index)


class PlayListPanel(QWidget, Ui_PlayList):
    def __init__(self, parent=None, lst=[]):
        super(PlayListPanel, self).__init__(parent)
        self.setupUi(self)
        self.setPlaylistTableView(lst)

    def loadPlaylistData(self, lst):
        """加载歌单数据
            传入歌单数据列表"""
        self.PlaylistSheetNamelabel.setText(lst[0])
        self.PlaylistIntrolabel.setText(lst[1])
        self.PlaylistFavorNumlabel.setText(lst[2])
        self.PlaylistMusicNumlabel.setText(lst[3])

    def getData(self, lst):
        """设置tableview的模型
            接受歌曲的五项属性二维列表"""
        self.model = QStandardItemModel(0, 5)
        self.Headers = ['ID', '标题', '歌手', '专辑', '时间', '操作']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(lst)
        for row in range(rowNum):
            for column in range(5):
                item = QStandardItem(f'{lst[row][column]}')
                self.model.setItem(row, column, item)

    def setPlaylistTableView(self, lst):
        self.getData(lst)
        self.PlaylistMusicListTableView = MyTableView()
        self.PlaylistDownLayout.addWidget(self.PlaylistMusicListTableView)
        self.PlaylistMusicListTableView.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.PlaylistMusicListTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.PlaylistMusicListTableView.verticalHeader().setDefaultSectionSize(40)
        self.PlaylistMusicListTableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def favorThisPlaylist(self):
        """收藏按钮的槽函数"""
        pass


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
    window = PlayListPanel(lst=[[1, 1, 1, 1, 1]])

    # 2.2 设置控件

    # 2.3 展示控件
    window.show()

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
