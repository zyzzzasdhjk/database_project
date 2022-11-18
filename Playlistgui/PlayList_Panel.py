from gui.Playlist import Ui_PlayList
from PyQt5.Qt import *


class PlayListPanel(QWidget, Ui_PlayList):
    def __init__(self, parent=None):
        super(PlayListPanel, self).__init__(parent)
        self.setup_Ui()

    def setup_Ui(self):
        self.model = QStandardItemModel(0, 5)
        self.Headers = ['ID', '操作', '标题', '歌手', '专辑', '时间']
        self.model.setHorizontalHeaderLabels(self.Headers)
        self.model.appendRow(QStandardItem('1'))
        self.setupUi(self)
        self.PlaylistMusicListTableView.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.PlaylistMusicListTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.PlaylistMusicListTableView.verticalHeader().setDefaultSectionSize(40)
        self.PlaylistMusicListTableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)


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
    window = PlayListPanel()

    # 2.2 设置控件
    window.setWindowTitle('')
    window.resize(500, 500)

    # 2.3 展示控件
    window.show()

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
