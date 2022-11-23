from login_Panel import LoginPanel
from register_Panel import RegisterPanel
from PyQt5.Qt import *
import qdarkstyle


class LoginRegisterPanel(QWidget):
    def __init__(self):
        super(LoginRegisterPanel, self).__init__()
        self.ini()

    def ini(self):
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setMaximumWidth(600)
        self.setMaximumHeight(400)
        self.loginPanel = LoginPanel(parent=self)
        self.loginPanel.setVisible(True)
        self.registerPanel = RegisterPanel(parent=self)
        self.registerPanel.setVisible(False)
        self.loginPanel.show_registerPanel_signal.connect(self.show_registerPanel)
        self.registerPanel.exit_signal.connect(self.return_loginPanel)

    def show_registerPanel(self):
        print('1')
        self.registerPanel.setVisible(True)
        self.loginPanel.setVisible(False)

    def check_login(self): # 登录函数
        pass

    def return_loginPanel(self):
        self.registerPanel.setVisible(False)
        self.loginPanel.setVisible(True)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # show window
    window = LoginRegisterPanel()

    # connect slot

    window.show()
    sys.exit(app.exec_())
