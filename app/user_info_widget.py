import sys

from gui import user_info_widget, main_ui
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, QtCore, QtGui


class User_info(QtWidgets.QWidget, user_info_widget.Ui_Form):  # 修改main_ui.Ui_MainWindow

    def __init__(self):
        super(User_info, self).__init__()
        self.setupUi(self)
        self.ini()

    def ini(self):
        # .currentIndex() 返回选中项的索引
        # 添加性别选项
        self.gender_combox.addItem("男")
        self.gender_combox.addItem("女")
        # 添加标签选项
        self.user_label_combox.addItem("标签1")
        self.user_label_combox.addItem("标签2")
        self.user_label_combox.addItem("标签3")
        self.user_label_combox.addItem("标签4")
        self.user_label_combox.addItem("标签5")
        self.user_label_combox.addItem("标签6")
        self.user_label_combox.addItem("标签7")
        # 设置uid为只读
        self.uid_eidt.setText("1111")
        self.uid_eidt.setReadOnly(True)
        # 设置两个按钮的槽函数
        self.reset_button.clicked.connect(self.reset_setting)
        self.apply_button.clicked.connect(self.apply_setting)

    def reset_setting(self):
        pass

    def apply_setting(self):
        pass

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
