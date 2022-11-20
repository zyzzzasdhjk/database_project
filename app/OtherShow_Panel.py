from PyQt5.Qt import *
from gui.OtherShow import Ui_OtherShow


class Window(QWidget, Ui_OtherShow):
    def __init__(self, parent=None):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setPlaylist()
        self.setupUi(self)

    def setPlaylist(self):
        self.model = QStandardItemModel(0, 5)
        self.Headers = ['ID', '操作', '标题', '创建人']
        self.model.setHorizontalHeaderLabels(self.Headers)
        self.model.appendRow(QStandardItem('1'))
        self.setupUi(self)
        self.OtherShowPlayListtableView.setModel(self.model)
        # 自适应布局，设置高度与宽度
        self.OtherShowPlayListtableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.OtherShowPlayListtableView.verticalHeader().setDefaultSectionSize(40)
        self.OtherShowPlayListtableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)


if __name__ == '__main__':
    import sys
    import qdarkstyle

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = Window()
    window.show()
    sys.exit(app.exec_())
