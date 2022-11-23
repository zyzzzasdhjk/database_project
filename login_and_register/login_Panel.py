from PyQt5.Qt import *
from login_and_register.resource.ui.login import Ui_login
import qdarkstyle
from sql.sql import DataBase


class LoginPanel(QWidget, Ui_login):
    show_registerPanel_signal = pyqtSignal()
    checkLoginSuccesssignal = pyqtSignal(int)

    def __init__(self, parent=None):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setupUi(self)

    def login_to_register(self):
        self.show_registerPanel_signal.emit()

    def check_login(self):
        self.db = DataBase("127.0.0.1", "sa", "5151", "MMS")
        account = self.login_username_text.text()
        password = self.login_password_text.text()
        self.UID = self.db.login(account, password)
        self.db.conn.close()
        if self.UID:
            self.checkLoginSuccesssignal.emit(self.UID)
        else:
            QMessageBox.about(self, '错误', "账号或密码有误，请重试")





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = LoginPanel()
    window.show()
    sys.exit(app.exec_())
