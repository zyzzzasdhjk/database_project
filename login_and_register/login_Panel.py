from PyQt5.Qt import *
from resource.ui.login import Ui_login
import qdarkstyle


class LoginPanel(QWidget, Ui_login):
    show_registerPanel_signal = pyqtSignal()
    checkLoginsignal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setupUi(self)

    def login_to_register(self):
        self.show_registerPanel_signal.emit()

    def check_login(self):
        self.account = self.login_username_text.text()
        self.password = self.login_password_text.text()
        self.checkLoginsignal.emit(self.account, self.password)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = LoginPanel()
    window.show()
    sys.exit(app.exec_())
