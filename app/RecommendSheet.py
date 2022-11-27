from PyQt5.Qt import *
from gui.FindMusic import Ui_FindMusic


class RecommendSheet(QWidget, Ui_FindMusic):
    getSheetsignal = pyqtSignal(int)

    def __init__(self, parent=None):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setupUi(self)
        self.pushButtonSeries = [self.FindMusicBtn1, self.FindMusicBtn2, self.FindMusicBtn3,
                                 self.FindMusicBtn4, self.FindMusicBtn5, self.FindMusicBtn6]
        self.iniSignal()

    def loadSheet(self, lst):
        """根据Label传入一个歌单列表
            最多六个歌单
            [SName]"""
        for i in range(len(lst)):
            self.pushButtonSeries[i].setText(lst[i])
            self.pushButtonSeries[i].setEnabled(True)

    def iniSignal(self):
        """每个按钮传出一个索引"""
        self.pushButtonSeries[0].clicked.connect(lambda: self.getSheetsignal.emit(0))
        self.pushButtonSeries[1].clicked.connect(lambda: self.getSheetsignal.emit(1))
        self.pushButtonSeries[2].clicked.connect(lambda: self.getSheetsignal.emit(2))
        self.pushButtonSeries[3].clicked.connect(lambda: self.getSheetsignal.emit(3))
        self.pushButtonSeries[4].clicked.connect(lambda: self.getSheetsignal.emit(4))
        self.pushButtonSeries[5].clicked.connect(lambda: self.getSheetsignal.emit(5))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = RecommendSheet()
    window.loadSheet(['1', '2', '3', '4'])
    window.getSheetsignal.connect(lambda x: print(x))
    window.show()
    sys.exit(app.exec_())
