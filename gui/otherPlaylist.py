# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'otherPlaylist.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlayList(object):
    def setupUi(self, PlayList):
        PlayList.setObjectName("PlayList")
        PlayList.resize(758, 525)
        PlayList.setStyleSheet("font: \"微软雅黑\";")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(PlayList)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.UI = QtWidgets.QWidget(PlayList)
        self.UI.setObjectName("UI")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.UI)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.PlaylistgraphicView = QtWidgets.QGraphicsView(self.UI)
        self.PlaylistgraphicView.setMinimumSize(QtCore.QSize(0, 0))
        self.PlaylistgraphicView.setMaximumSize(QtCore.QSize(10000000, 10000000))
        self.PlaylistgraphicView.setStyleSheet("")
        self.PlaylistgraphicView.setObjectName("PlaylistgraphicView")
        self.verticalLayout_8.addWidget(self.PlaylistgraphicView)
        self.PlaylistFavorpushButton = QtWidgets.QPushButton(self.UI)
        self.PlaylistFavorpushButton.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.PlaylistFavorpushButton.setObjectName("PlaylistFavorpushButton")
        self.verticalLayout_8.addWidget(self.PlaylistFavorpushButton)
        self.verticalLayout_8.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.PlaylistSheetNamelabel = QtWidgets.QLabel(self.UI)
        self.PlaylistSheetNamelabel.setStyleSheet("font: 20pt \"微软雅黑\";")
        self.PlaylistSheetNamelabel.setObjectName("PlaylistSheetNamelabel")
        self.verticalLayout_5.addWidget(self.PlaylistSheetNamelabel)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.UI)
        self.label_2.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.PlaylistCreatorNamelabel = QtWidgets.QLabel(self.UI)
        self.PlaylistCreatorNamelabel.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.PlaylistCreatorNamelabel.setObjectName("PlaylistCreatorNamelabel")
        self.horizontalLayout_6.addWidget(self.PlaylistCreatorNamelabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.PlaylistIntrolabel = QtWidgets.QPlainTextEdit(self.UI)
        self.PlaylistIntrolabel.setStyleSheet("font: 12pt \"方正姚体\";")
        self.PlaylistIntrolabel.setReadOnly(True)
        self.PlaylistIntrolabel.setObjectName("PlaylistIntrolabel")
        self.verticalLayout_5.addWidget(self.PlaylistIntrolabel)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_5 = QtWidgets.QLabel(self.UI)
        self.label_5.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_9.addWidget(self.label_5)
        self.PlaylistMusicNumlabel = QtWidgets.QLabel(self.UI)
        self.PlaylistMusicNumlabel.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.PlaylistMusicNumlabel.setObjectName("PlaylistMusicNumlabel")
        self.horizontalLayout_9.addWidget(self.PlaylistMusicNumlabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_6 = QtWidgets.QLabel(self.UI)
        self.label_6.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_10.addWidget(self.label_6)
        self.PlaylistFavorNumlabel = QtWidgets.QLabel(self.UI)
        self.PlaylistFavorNumlabel.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.PlaylistFavorNumlabel.setObjectName("PlaylistFavorNumlabel")
        self.horizontalLayout_10.addWidget(self.PlaylistFavorNumlabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_10)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(3, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.PlaylistDownLayout = QtWidgets.QVBoxLayout()
        self.PlaylistDownLayout.setObjectName("PlaylistDownLayout")
        self.verticalLayout_2.addLayout(self.PlaylistDownLayout)
        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_4.addWidget(self.UI)

        self.retranslateUi(PlayList)
        self.PlaylistFavorpushButton.clicked.connect(PlayList.favorThisPlaylist)
        QtCore.QMetaObject.connectSlotsByName(PlayList)

    def retranslateUi(self, PlayList):
        _translate = QtCore.QCoreApplication.translate
        PlayList.setWindowTitle(_translate("PlayList", "Form"))
        self.PlaylistFavorpushButton.setText(_translate("PlayList", "删除"))
        self.PlaylistSheetNamelabel.setText(_translate("PlayList", "歌单名字"))
        self.label_2.setText(_translate("PlayList", "创建者："))
        self.PlaylistCreatorNamelabel.setText(_translate("PlayList", "TextLabel"))
        self.PlaylistIntrolabel.setPlainText(_translate("PlayList", "Introduction"))
        self.label_5.setText(_translate("PlayList", "歌曲数："))
        self.PlaylistMusicNumlabel.setText(_translate("PlayList", "TextLabel"))
        self.label_6.setText(_translate("PlayList", "收藏数："))
        self.PlaylistFavorNumlabel.setText(_translate("PlayList", "TextLabel"))