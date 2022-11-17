from PyQt5.Qt import *
from gui.UserEdit import Ui_UserEdit


class UserEditPanel(QWidget, Ui_UserEdit):
    def __init__(self, parent=None):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, UserEdit):
        super().setupUi(UserEdit)
        self.UserEditUSexComboBox.addItem('男', '1')
        self.UserEditUSexComboBox.addItem('女', '2')
        self.labellist = ['忧郁', '土嗨', '抖音', '二刺螈', '怀旧']
        self.UserEditLIDComboBox.addItems(self.labellist)


if __name__ == '__main__':
    import sys

    # 1. 创建一个应用程序对象
    app = QApplication(sys.argv)
    # setup stylesheet
    import qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = UserEditPanel()
    window.show()
    sys.exit(app.exec_())
