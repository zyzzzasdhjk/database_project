from resource.Playlist import Ui_PlayList
from PyQt5.Qt import *


class PlayList(QWidget, Ui_PlayList):
    def __init__(self, parent=None):
        super(PlayList, self).__init__(parent)
        self.model = QStandardItemModel(0, 5)
        self.Headers = ['操作', '标题', '歌手', '专辑', '时间']
        self.model.setHorizontalHeaderLabels(self.Headers)
        self.setupUi(self)
        self.PlaylistMusicList.setModel(self.model)


if __name__ == '__main__':
    # 0. 导入所需要的包和模块
    from PyQt5.Qt import *
    import sys
    import qdarkstyle

    # 1. 创建一个应用程序对象
    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # 2. 控件的操作
    # 2.1 创建控件
    window = PlayList()

    # 2.2 设置控件
    window.setWindowTitle('')
    window.resize(500, 500)

    # 2.3 展示控件
    window.show()

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
