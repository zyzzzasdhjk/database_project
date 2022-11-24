from PyQt5.Qt import *
from gui.getUserSearch import Ui_getUserSearch
import datetime

class getUserSearchPanel(QWidget, Ui_getUserSearch):
    def __init__(self, parent=None, UserData=[]):
        # 调用父类的初始化方法
        super().__init__(parent)
        self.setupUi(self)
        self.iniTableview(UserData)

    def iniTableview(self, UserData):
        """接受一个二维列表
        [[UID, UName, USex]]"""

        self.model = QStandardItemModel(0, 0)
        self.Headers = ['ID', '昵称', '性别']
        self.model.setHorizontalHeaderLabels(self.Headers)
        rowNum = len(UserData)
        columnNum = 3
        for row in range(rowNum):
            for column in range(columnNum):
                item = QStandardItem(str(UserData[row][column]))
                self.model.setItem(row, column, item)

        self.getUserSearchTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 自适应布局，设置高度与宽度
        self.getUserSearchTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.getUserSearchTableView.verticalHeader().setDefaultSectionSize(40)
        self.getUserSearchTableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.getUserSearchTableView.setModel(self.model)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    import qt_material

    # setup stylesheet
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')
    window = getUserSearchPanel(UserData=[[1, '红茶honer', '男']])
    window.show()
    sys.exit(app.exec_())
