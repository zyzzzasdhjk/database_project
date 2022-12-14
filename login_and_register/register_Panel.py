from PyQt5.Qt import *
from login_and_register.resource.ui.register import Ui_register_window
import qdarkstyle
from sql.sql import DataBase


class RegisterPanel(QWidget, Ui_register_window):
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.animation_targets = [self.register_about_btn, self.register_restart_btn, self.register_exit_btn]
        self.animation_targets_pos = [target.pos() for target in self.animation_targets]

    def show_hide_menu(self, check):
        print('显示和隐藏', check)

        # 序列动画组
        animation_group = QSequentialAnimationGroup(self)
        for index, target in enumerate(self.animation_targets):
            animation = QPropertyAnimation()
            animation.setTargetObject(target)
            animation.setPropertyName(b'pos')
            if not check:
                target.setEnabled(True)
                animation.setStartValue(self.register_menu_btn.pos())
                animation.setEndValue(self.animation_targets_pos[index])
            else:
                target.setEnabled(False)
                animation.setStartValue(self.animation_targets_pos[-(index + 1)])
                animation.setEndValue(self.register_menu_btn.pos())
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.InOutBounce)

            animation_group.addAnimation(animation)
        animation_group.start(QAbstractAnimation.DeleteWhenStopped)

    def show_about(self):
        print('关于')
        QMessageBox.about(self, 'about', 'https://github.com/zyzzzasdhjk/database_project')

    def restart(self):
        print('reset')
        self.register_username_text.clear()
        self.register_password_text.clear()
        self.register_password2_text.clear()

    def register_exit(self):
        self.exit_signal.emit()

    def check_register(self):
        print('register')
        self.db = DataBase("127.0.0.1", "sa", "5151", "MMS")
        account = self.register_username_text.text()
        password = self.register_password_text.text()
        if password == self.register_password2_text.text() and password != '':
            judge = self.db.register(account, password)
            self.db.conn.close()
            if judge:
                QMessageBox.about(self, '成功', "注册成功")
            else:
                QMessageBox.about(self, '失败', "账号重复，请重新输入")

        else:
            QMessageBox.about(self, '错误', "密码输入不一致，请重试")


if __name__ == '__main__':
    # 0. 导入所需要的包和模块
    import sys

    # 1. 创建一个应用程序对象
    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # 2. 控件的操作
    # 2.1 创建控件
    window = RegisterPanel()

    # 2.2 设置控件
    window.setWindowTitle('register')
    window.resize(500, 500)

    # 2.3 展示控件
    window.exit_signal.connect(lambda: print('exit'))
    window.check_register_signal.connect(lambda a, p: print(a, p))
    window.show()

    # 3. 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())
