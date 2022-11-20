from PyQt5.QtGui import QStandardItemModel, QStandardItem
from qtpy import QtWidgets

from gui import playlist_widget


class win(QtWidgets.QWidget, playlist_widget.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self, parent=None):
        super(win, self).__init__(parent)
        self.setupUi(self)
        self.model = QStandardItemModel(4, 7)
        self.ini()

    def ini(self):
        # self.model.setHorizontalHeaderLabels([ 'bh','gm','gs','zj','sc','sc','sc'])
        # arr = ['jak', 'tom']
        # for row in range(4):
        #     for column in range(7):
        #         item = QStandardItem(str(1))
        #         self.model.setItem(row, column, item)
        # self.tableView.setModel(self.model)
        # self.tableView.verticalHeader().setVisible(False)
        # self.tableView.horizontalHeader().setVisible(False)
        pass
