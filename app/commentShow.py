# 0. 导入所需要的包和模块
from PyQt5.Qt import *
from gui.commentShow import Ui_commentShow
from gui.commentWidget import Ui_CommentWidget


class commentWidget(QWidget, Ui_CommentWidget):
    def __init__(self, parent=None):
        super(commentWidget, self).__init__(parent)
        self.setupUi(self)


class commentShowPanel(QWidget, Ui_commentShow):
    commitCommentsignal = pyqtSignal(int, str)

    def __init__(self, parent=None, MID=None):
        super(commentShowPanel, self).__init__(parent)
        self.ID = MID
        self.setupUi(self)
        self.CommentCommitButton.clicked.connect(self.CommitComment)

    def loadComment(self, lst):
        """传入评论二维列表
            [[UName, CContent]]"""
        for item in lst:
            newComment = commentWidget()
            newComment.commentUserLabel.setText(item[0])
            newComment.commentTextLabel.setPlainText(item[1])
            self.commentShowWidget.layout().addWidget(newComment)

    def loadMusicInfo(self, MName):
        self.commentShowMusicLabel.setText(MName)

    def CommitComment(self):
        """提交评论的槽函数
            传出MID，CContent"""
        CContent = self.CommentInputLabel.toPlainText()
        self.commitCommentsignal.emit(self.ID, CContent)


import sys
import qdarkstyle

if __name__ == '__main__':
    # 1. 创建一个应用程序对象
    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # 2. 控件的操作
    # 2.1 创建控件
    window = commentShowPanel()
    window.loadComment([['1', '2'], ['1', '2'], ['1', '2']])

    # 2.2 设置控件
    window.setWindowTitle('')

    # 2.3 展示控件
    window.show()

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
