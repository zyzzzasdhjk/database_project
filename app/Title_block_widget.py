from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, QtCore, QtGui
from gui import Title_block


class CLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    # 可在外部与槽函数连接
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class title_widget(QtWidgets.QWidget, Title_block.Ui_Form):  # 修改main_ui.Ui_MainWindow
    widget_change_signal = pyqtSignal(int)
    user_uid = pyqtSignal(int)

    def __init__(self):
        super(title_widget, self).__init__()
        self.setupUi(self)
        self.user_name = QLabel("6666")
        self.user_name.setStyleSheet('font: 10pt "微软雅黑";')
        self.user_center = CLabel("个人中心")
        self.user_center.setStyleSheet('font: 10pt "微软雅黑";')
        self.ini()

    def ini(self):
        self.Layout.addWidget(self.user_name)
        self.Layout.addWidget(self.user_center)
        self.user_center.connect_customized_slot(self.open_user_info)

    def open_user_info(self):
        self.widget_change_signal.emit(-1)
        self.user_uid.emit(1)