import sys

from PyQt5.QtCore import QDate

from gui import user_info_widget, main_ui
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, QtCore, QtGui


class User_info(QtWidgets.QWidget, user_info_widget.Ui_Form):  # 修改main_ui.Ui_MainWindow
    user_info_change = QtCore.pyqtSignal(list)

    def __init__(self):
        super(User_info, self).__init__()
        self.user_info_lst = None
        self.setupUi(self)

    def ini(self, lst):
        # .currentIndex() 返回选中项的索引
        # 加载账号，设为只读
        self.acount_edit.setText(lst[1])  # 加载账号
        self.uid_eidt.setReadOnly(True)  # 设为只读
        self.password_edit.setText(lst[2])  # 加载密码，加密为*
        # 加载个人信息
        self.uid_eidt.setText(str(lst[0]))  # 加载uid
        self.acount_edit.setReadOnly(True)  # uid设为只读
        self.user_name_edit.setText(lst[3])  # 加载名字
        self.gender_combox.setCurrentIndex(0 if lst[4] == '1' else 1)  # 加载性别
        self.dateEdit.setDate(QDate(lst[6].year,lst[6].month,lst[6].day))
        self.user_des_edit.setPlainText(lst[5])  # 加载个人介绍
        self.user_label_combox.setCurrentIndex(lst[8]-1)  # 加载用户标签
        # 设置提示框
        # self.birthday_edit.setText("格式为:*.*，例如1.1")
        # 设置两个按钮的槽函数
        self.reset_button.clicked.connect(self.reset_setting)
        self.apply_button.clicked.connect(self.apply_setting)

    def ini_user_info(self,lst):
        self.user_info_lst = lst
        self.ini(self.user_info_lst)

    def ini_combox(self, lst):
        self.gender_combox.clear()
        self.user_label_combox.clear()
        # 添加性别选项
        self.gender_combox.addItem("男")
        self.gender_combox.addItem("女")
        for i in lst:
            self.user_label_combox.addItem(i[1])

    def reset_setting(self):
        self.ini(self.user_info_lst)

    def apply_setting(self):
        uid = self.uid_eidt.text()
        user_account = self.acount_edit.text()
        user_password = self.password_edit.text()
        user_name = self.user_name_edit.text()
        user_gender = self.gender_combox.currentIndex()
        user_into = self.user_des_edit.toPlainText()
        b = self.dateEdit.date().toString().split(" ")
        m = f"0{b[1][:-1]}" if len(b[1][:-1])==1 else f"{b[1][:-1]}"
        d = f"0{b[2]}" if len(b[2])==1 else f"{b[2]}"
        user_birthday = f"{b[3]}-{m}-{d}"
        user_label_index = self.user_label_combox.currentIndex()+1
        user_isVIP = self.user_info_lst[7]
        self.user_info_change.emit([[uid,user_account,user_password],
               [uid,user_name,user_gender,user_into,user_birthday,user_isVIP,user_label_index]])


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.ini_window()

    def ini_window(self):
        A = User_info()
        self.right_layout.addWidget(A)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import qdarkstyle

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
