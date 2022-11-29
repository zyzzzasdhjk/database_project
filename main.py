from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from sql import sql
from app import MusicPlayer, Sidebar, playlist_widget, PlayList_Panel, Title_block_widget, user_info_widget, \
    Music_search, MyPlaylist, otherPlaylist_Panel, music_recommendation, addMenu, RecommendSheet, commentShow, \
    OtherShow_Panel
from gui import main_ui  # 导入ui文件
from login_and_register.login_register_Panel import LoginRegisterPanel

global MainProgress

global uid_int  # 得到的uid，待完善
uid_int = 1


class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    def __int__(self, parent):
        # 初始化函数
        super(WorkThread, self).__init__()
        self.parent = parent

    def run(self):
        self.parent().my_playlist.update_tableView_music(self.parent().music.music_lst)
        self.parent().right_layout.addWidget(self.parent().my_playlist)
        self.parent().my_playlist.tabel.startplaysignal.connect(self.parent().music.add_music_to_lst)
        self.parent().my_playlist.tabel.deleteThisMusicsignal.connect(self.parent().music.delete_music)


def loginControl(UID):  # 登录函数
    global uid_int

    uid_int = UID
    MainProgress.mainwindow = Main_window()
    MainProgress.mainwindow.show()
    MainProgress.loginregisterPanel.hide()
    print(UID)


class MainProgress(QtWidgets.QWidget):
    """主进程，包含MainWindow和LoginRegisterPanel
        当登陆成功时，UID才被赋值，MainWindow才被初始化
        由于单开进程会被取消，所以采用主进程的方式"""

    def __init__(self):
        super().__init__()

        self.loginregisterPanel = LoginRegisterPanel()
        self.mainwindow = 0


class Main_window(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    # ************初始化载入模块*******************start
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)
        self.search_str = ''  # 搜索内容
        self.search_type = '歌手'  # 搜索类别
        self.MyPlaylistThread = WorkThread(self)
        # 初始化数据库连接
        self.db = sql.DataBase("127.0.0.1", "sa", "5151", "MMS")

        # 获取歌单数据
        self.createSheetList = self.db.getUserAllCreateSheet(uid_int)
        self.favorSheetList = self.db.getUserAllFavorSheet(uid_int)
        self.recommendSheetList = self.db.getUserRecommendSheet(uid_int)

        # 初始化界面
        self.music = MusicPlayer.Music_player()
        self.sidebar = Sidebar.Sidebar_widget()
        self.title_block = Title_block_widget.title_widget()
        self.user_info = user_info_widget.User_info()
        self.addM = addMenu.add_menu()
        self.ini_window()

    def ini_window(self):
        # 加载顶部栏标签和用户名字
        self.title_block.update_name(self.db.get_user_info(uid_int)[0][3])
        self.title_block.update_label_combox(self.db.get_all_user_label())
        self.top_layout.addWidget(self.title_block)  # 添加顶部栏到主页面
        # 加载音乐播放界面
        self.music.playlist_button.clicked.connect(lambda: self.change_widget_by_signal(3))
        self.music.favor_button.clicked.connect(
            lambda: self.startAddMenu(self.db.getMidByMname(self.music.music_lst[self.music.music_num][0])))
        self.bottom_layout.addWidget(self.music)
        # 加载侧边栏
        self.sidebar.iniCreateSheet(self.createSheetList)
        self.sidebar.iniFavorSheet(self.favorSheetList)
        self.left_layout.addWidget(self.sidebar)  # 添加侧边栏到主页面

        '''信号区'''
        # 侧边栏
        # 侧边栏页面切换
        self.sidebar.widget_change_signal.connect(self.change_widget_by_signal)  # 页面切换信号
        self.sidebar.createSheetShowSignal.connect(self.showCreateSheet)
        self.sidebar.favorSheetShowSignal.connect(self.showFavorSheet)
        # 侧边栏创建歌单按钮
        self.sidebar.createSheetSignal.connect(self.createSheet)

        self.title_block.openUserEditsiganl.connect(self.update_user_info)  # 刷新个人信息
        self.title_block.widget_change_signal.connect(self.change_widget_by_signal)  # 切换到个人信息界面
        self.title_block.search_str.connect(self.update_search_str)  # 更新搜索内容
        # self.music.music_lst_s.connect(self.my_playlist.update_tableView_music)

    # ************初始化载入模块*******************end

    # ************切换界面模块*******************start
    def change_widget_by_signal(self, index):
        # 删除原有布局的控件
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        # self.music_recommend_widget = PlayList_Panel.PlayListPanel()
        if index == -1:
            # 用户个人信息设置界面
            self.user_info = user_info_widget.User_info()
            self.right_layout.addWidget(self.user_info)
            self.user_info.user_info_change.connect(self.update_user_info_db)
        elif index == 0:
            self.music_r = music_recommendation.Music_r()
            self.music_r.update_tableView_music(self.db.getMusicR())
            self.right_layout.addWidget(self.music_r)
            self.music_r.table.startNextPlaySignal.connect(self.music.insert_music_to_lst)
            self.music_r.table.addMenuSignal.connect(self.startAddMenu)
        elif index == 1:
            # 推荐歌单界面
            self.recommendSheetPanel = RecommendSheet.RecommendSheet()
            self.recommendSheetPanel.loadSheet([item[1] for item in self.recommendSheetList])
            self.recommendSheetPanel.getSheetsignal.connect(
                lambda index: self.ShowNewSheet(self.recommendSheetList[index][0]))
            self.right_layout.addWidget(self.recommendSheetPanel)
        elif index == 2:
            self.search_widget = Music_search.Search()
            self.search_widget.search_type.connect(self.update_search_type)
            self.right_layout.addWidget(self.search_widget)
        #     # self.search_widget.setVisible(True)
        elif index == 3:
            # 播放列表
            self.my_playlist = MyPlaylist.My_playlist()
            self.my_playlist.update_tableView_music(self.music.music_lst)
            self.right_layout.addWidget(self.my_playlist)
            self.my_playlist.tabel.startplaysignal.connect(self.music.add_music_to_lst)
            self.my_playlist.tabel.deleteThisMusicsignal.connect(self.music.delete_music)

    def startAddMenu(self, n):
        self.addM.update_tableView_music(self.db.getUserAllCreateSheet(uid_int))
        self.addM.show()
        self.addM.getMid(n)
        self.addM.table.addMenuSignal.connect(self.favorMusic)

    def showCreateSheet(self, index):
        # 删除原有布局的控件
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        # 歌单
        self.playlist = PlayList_Panel.PlayListPanel()

        self.playlist.updateThisSheetsignal.connect(self.updateSheetInfo)
        self.playlist.deleteThisSheetsignal.connect(self.deleteSheet)
        self.playlist.PlaylistMusicListTableView.startplaysignal.connect(
            self.music.add_music_to_lst)  # 传入数组的要求 [歌曲名字，歌手名字，歌曲路径] 要求全为字符串
        self.playlist.PlaylistMusicListTableView.deleteThisMusicsignal.connect(self.deleteMusic)
        self.playlist.PlaylistMusicListTableView.showCommentsignal.connect(self.ShowComment)

        self.getPlaylistInfo(self.playlist, self.createSheetList[index][0])
        self.right_layout.addWidget(self.playlist)

    def showFavorSheet(self, index):
        # 删除原有布局的控件
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        # 歌单
        self.playlist = otherPlaylist_Panel.otherPlayListPanel()

        self.playlist.deleteThisFavorSheetsignal.connect(self.unfavorThisSheet)
        self.playlist.PlaylistMusicListTableView.startplaysignal.connect(
            self.music.add_music_to_lst)  # 传入数组的要求 [歌曲名字，歌手名字，歌曲路径] 要求全为字符串
        self.playlist.PlaylistMusicListTableView.addMenuSignal.connect(self.startAddMenu)
        self.playlist.PlaylistMusicListTableView.showCommentsignal.connect(self.ShowComment)

        self.getPlaylistInfo(self.playlist, self.favorSheetList[index][0])

        self.right_layout.addWidget(self.playlist)

    def ShowNewSheet(self, SID):
        """他人歌单显示函数"""
        # 删除原有布局的控件
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        self.playlist = otherPlaylist_Panel.otherPlayListPanel()
        self.playlist.PlaylistFavorpushButton.setText("收藏")

        self.playlist.deleteThisFavorSheetsignal.connect(self.favorThisSheet)
        self.playlist.PlaylistMusicListTableView.startplaysignal.connect(
            self.music.add_music_to_lst)  # 传入数组的要求 [歌曲名字，歌手名字，歌曲路径] 要求全为字符串
        self.playlist.PlaylistMusicListTableView.addMenuSignal.connect(self.startAddMenu)
        self.playlist.PlaylistMusicListTableView.showCommentsignal.connect(self.ShowComment)

        self.getPlaylistInfo(self.playlist, SID)

        self.right_layout.addWidget(self.playlist)

    def ShowComment(self, MID):
        """展示评论的槽函数
            接收MID，刷新展示评论界面"""
        MName = self.db.getMusicName(MID)
        MCommentlst = self.db.getMusicComment(MID)

        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()

        self.Comment = commentShow.commentShowPanel(MID=MID)
        self.Comment.commitCommentsignal.connect(self.commitComment)
        self.Comment.loadComment(MCommentlst)
        self.Comment.loadMusicInfo(MName)
        self.right_layout.addWidget(self.Comment)

    def userW(self, UID):
        """传入uid，打开用户界面"""
        print(UID)

        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()

        userinfo = self.db.get_user_info2(UID)
        sheetinfo = self.db.getOtherUserSheetInfo(UID)

        self.otherUserWidget =  OtherShow_Panel.OtherShowPanel()
        self.otherUserWidget.loadOtherInfo(userinfo)
        self.otherUserWidget.loadOtherShowTableViewModel(sheetinfo)

        self.otherUserWidget.OtherShowTableView.enterSheetsignal.connect(self.ShowNewSheet)
        self.right_layout.addWidget(self.otherUserWidget)



    # ************切换界面模块*******************end

    # ************连接数据模块*******************start
    def getPlaylistInfo(self, Playlist, SID):
        """更新歌单界面
            传入歌单界面对象, SID"""
        Playlist.loadPlaylistTableViewModel(self.db.getPlaylistMusicData(SID))
        Playlist.loadPlaylistData(self.db.getPlaylistSheetData(SID))

    def createSheet(self):
        """新建歌单
            侧边栏新建歌单按钮的槽函数"""
        result = self.db.createSheet(uid_int)
        print(result)
        if result:
            QtWidgets.QMessageBox.about(self, "成功", "创建成功")
        else:
            QtWidgets.QMessageBox.about(self, "失败", "创建失败，歌单超过限制数目")
        self.createSheetList = self.db.getUserAllCreateSheet(uid_int)
        self.sidebar.iniCreateSheet(self.createSheetList)

    def updateSheetInfo(self, SID, SIntro):
        """更新歌单数据
            myPlaylistPanel更新数据按钮的槽函数"""
        self.db.updateSheetInfo(SID, SIntro)
        QtWidgets.QMessageBox.about(self, '成功', '更新成功')
        list = [item[0] for item in self.createSheetList]
        index = list.index(SID)
        self.showCreateSheet(index)

    def deleteSheet(self, SID):
        """删除该歌单
            myPlaylistPanel删除按钮的槽函数"""
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        self.db.deleteSheet(SID)
        QtWidgets.QMessageBox.about(self, '成功', '删除成功')
        self.createSheetList = self.db.getUserAllCreateSheet(uid_int)
        self.sidebar.iniCreateSheet(self.createSheetList)

    def favorThisSheet(self, SID):
        """收藏此歌单"""
        if self.db.favorThisSheet(uid_int, SID):
            QtWidgets.QMessageBox.about(self, "成功", "收藏成功")
            self.favorSheetList = self.db.getUserAllFavorSheet(uid_int)
            self.sidebar.iniFavorSheet(self.favorSheetList)
        else:
            QtWidgets.QMessageBox.about(self, "失败", "已经收藏过了")

    def unfavorThisSheet(self, SID):
        """取消收藏改歌单
            otherPlaylistPanel删除按钮的槽函数"""
        deleted = self.right_layout.itemAt(0)
        if deleted:
            deleted.widget().deleteLater()
        self.db.unFavorSheet(uid_int, SID)
        QtWidgets.QMessageBox.about(self, '成功', '取消收藏成功')
        self.favorSheetList = self.db.getUserAllFavorSheet(uid_int)
        self.sidebar.iniFavorSheet(self.favorSheetList)

    def favorMusic(self, MID, SID):
        """收藏歌曲"""
        if self.db.insert_music_to_FavorSheet(MID, SID):
            QtWidgets.QMessageBox.about(self, "成功", "收藏成功")
        else:
            QtWidgets.QMessageBox.about(self, "失败", "收藏失败，歌单中已存在该音乐")

    def deleteMusic(self, MID):
        """删除歌曲"""
        SID = self.playlist.ID
        if self.db.deleteMusic(SID, MID):
            QtWidgets.QMessageBox.about(self, "成功", "删除成功")
            SIDlst = [item[0] for item in self.createSheetList]
            index = SIDlst.index(SID)
            self.showCreateSheet(index)
        else:
            QtWidgets.QMessageBox.about(self, "失败", "删除失败")

    def update_user_info(self):  # 传入个人信息以加载
        self.user_info.ini_combox(self.db.get_all_user_label())  # 先初始化combox
        self.user_info.ini_user_info(self.db.get_user_info(uid_int))  # 传入列表以加载

    def update_user_info_db(self, lst):
        if self.db.update_user_info(lst):
            QtWidgets.QMessageBox.about(self, '成功修改', '修改个人资料成功')
        else:
            QtWidgets.QMessageBox.about(self, '失败修改', '修改个人资料失败')
        self.user_info.ini_user_info(self.db.get_user_info(lst[0][0]))
        self.recommendSheetList = self.db.getUserRecommendSheet(uid_int)

    def closeEvent(self, event):
        self.music.save_json()

    def update_search_str(self, s):
        self.search_str = s
        if self.search_type == '歌曲':
            data = self.db.getSearchMusic(s)
        elif self.search_type == '歌手':
            data = self.db.getSearchMusician(s)
        elif self.search_type == '用户':
            data = self.db.getSearchPerson(s)
        self.change_widget_by_signal(2)
        if self.search_type != '用户':
            self.search_widget.update_tableView_music(data)
            self.search_widget.tabel.startNextPlaySignal.connect(self.music.insert_music_to_lst)
            self.search_widget.tabel.addMenuSignal.connect(self.startAddMenu)
        else:
            self.search_widget.update_tableView_person(data)
            self.search_widget.tabel.visitOther.connect(self.userW)

    def update_search_type(self, s):
        self.search_type = s
        self.update_search_str(self.search_str)

    def commitComment(self, MID, CContent):
        """上传评论，并加载"""
        if self.db.commitComment(uid_int, MID, CContent):
            QtWidgets.QMessageBox.about(self, "成功", "上传成功")
        else:
            QtWidgets.QMessageBox.about(self, "失败", "上传失败，请重试")

        self.ShowComment(MID)

    # ************连接数据模块*******************end


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import qt_material

    # setup stylesheet
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')

    # 启动主进程
    MainProgress = MainProgress()
    MainProgress.loginregisterPanel.show()
    MainProgress.loginregisterPanel.loginPanel.checkLoginSuccesssignal.connect(loginControl)

    sys.exit(app.exec_())
