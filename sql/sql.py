import pymssql


# server默认为127.0.0.1，如果打开了TCP动态端口的需要加上端口号，如'127.0.0.1:1433'
# user默认为sa
# password为自己设置的密码
# database为数据库名字
# 可简化为conn = pymssql.connect(host='localhost', user='sa', password='123456', database='pubs')

class DataBase:
    def __init__(self, server, user, password, database):
        self.conn = pymssql.connect(server, user, password, database)  # charset='cp936'
        self.cursor = self.conn.cursor()

    def query_strip(self):
        """将查询结果转换成二维列表"""

        data = self.cursor.fetchall()
        return [[j.strip() if type(j) == str else j for j in i] for i in data]

    def register(self, account, password):
        """注册槽函数
            若没有该账号，则注册成功，返回True
            若有，则返回False"""

        judgestr = f"select account from Account_Password where account = '{account}'"
        self.cursor.execute(judgestr)
        judgelist = self.query_strip()
        # print(judgelist)
        if not judgelist:
            self.cursor.execute(f"insert into Account_Password values ('{account}','{password}')")
            self.conn.commit()
            return True
        else:
            return False

    def login(self, account, password):
        """登录槽函数
            若满足账号密码需求，则返回UID
            否则返回False"""

        judgestr = f"select UID from Account_Password where account = '{account}' and password = '{password}'"
        self.cursor.execute(judgestr)
        judgelist = self.query_strip()
        if judgelist:
            return judgelist[0][0]
        else:
            return False

    def getPlaylistMusicData(self, SID):
        """从视图中获取歌单歌曲数据
            返回二维列表[[MID,MName,MMName,MDate,AlbumName,MDir]]"""

        selectstr = f"select MID,MName,MMName,MDate,MDir from V$_getPlaylistMusicData where SID = {int(SID)}"
        self.cursor.execute(selectstr)
        MusicDatalist = self.query_strip()
        for i in range(len(MusicDatalist)):  # 添加专辑
            sql = f'select a.AName from MID_AID m left join Album a on m.AID=a.AID where MID={MusicDatalist[i][0]}'
            self.cursor.execute(sql)
            MusicDatalist[i].insert(4, self.query_strip()[0][0])
        return MusicDatalist

    def getPlaylistSheetData(self, SID):
        """从表与视图中获取歌单数据
            返回一维列表[SID, SName, SIntro, SFavor,UName, MusicNum]"""

        selectstr1 = f"select * from V$_getSheetUserCreateInfo where SID = {int(SID)}"
        selectstr2 = f"select MusicNum from V$_getSheetMusicNum where SID = {int(SID)}"
        self.cursor.execute(selectstr1)
        SheetDatalist = self.query_strip()[0]
        self.cursor.execute(selectstr2)
        musicnumresult = self.query_strip()
        if musicnumresult:
            musicnumresult = musicnumresult[0]
        else:
            musicnumresult = [0]
        SheetDatalist = SheetDatalist + musicnumresult
        return SheetDatalist

    def get_all_user_label(self):
        """获取标签
            返回二维列表，包含标签ID以及所有标签"""

        sql = 'select * from Label'
        self.cursor.execute(sql)
        d = sorted(self.query_strip(), key=lambda x: x[0], reverse=False)
        return d

    def update_user_info(self, lst):
        l1 = lst[0]
        l2 = lst[1]
        l = [f'''update Account_Password set Account = '{l1[1]}' where UID={l1[0]}''',
             f'''update Account_Password set Password = '{l1[2]}' where UID={l1[0]}''',
             f'''update UserInfo set UName = '{l2[1]}' where UID={l2[0]}''',
             f'''update UserInfo set USex = {l2[2]} where UID={l2[0]}''',
             f'''update UserInfo set Ulntro = '{l2[3]}' where UID={l2[0]}''',
             f'''update UserInfo set UBirthday = '{l2[4]}' where UID={l2[0]}''',
             f'''update UserInfo set UIsVip = '{l2[5]}' where UID={l2[0]}''',
             f'''update UserInfo set LID = {l2[6]} where UID={l2[0]}''']
        for i in l:
            self.cursor.execute(i)
        self.conn.commit()

    def get_user_info(self, uid):
        """根据uid查询
            返回的是一个列表,[uid，账号，密码，姓名，性别，个人介绍，生日，是否是vip，标签]"""

        sql = f'select * from V$_getUserInformation where UID={uid}'  # V$_getUserInformation
        self.cursor.execute(sql)
        # data = self.cursor.fetchall()
        l = self.query_strip()
        return l

    def change_user_info(self, uid, lst):
        sql = f"delete from UserInfo where uid = {uid}"

    def getSearchUser(self, searchstr):
        """搜索用户
            返回模糊匹配的二维列表
            [[UID, UName, USex]]"""

        sqlstr = f"select UID, UName, USex from UserInfo where UName like '%{searchstr}%'"
        self.cursor.execute(sqlstr)
        selectresult = self.query_strip()
        for lst in selectresult:
            if lst[2] == '1':
                lst[2] = '男'
            elif lst[2] == '2':
                lst[2] == '女'
        return selectresult

    def getSearchMusic(self, searchstr):
        """搜索音乐
            返回模糊匹配的二维列表
            [[MID,MName,MMName,MDate,AlbumName,MDir]]"""

        sqlstr = f"select MID,MName,MMName,MDate,AName,MDir from V$_getMusicData where MName like '%{searchstr}%'"
        self.cursor.execute(sqlstr)
        selectresult = self.query_strip()
        return selectresult

    def getUserAllCreateSheet(self, UID):
        """用户创建所有歌单数据
            返回一个二维列表
            [[SID, SName]]"""

        selectstr = f"select SID, SName from V$_getUserAllCreateSheet where UID = '{UID}'"
        self.cursor.execute(selectstr)
        resultlst = self.query_strip()
        return resultlst

    def insert_music_to_FavorSheet(self, mid, sid):
        try:
            sql = f'insert into SID_MID values({sid},{mid})'
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except pymssql._pymssql.IntegrityError:
            return

    def getMidByMname(self, x):
        sql = f"select MID from Music where MName = '{x}'"
        self.cursor.execute(sql)
        return self.query_strip()[0][0]

    def getAllSheetByMusic(self, mid):
        sql = f'select SID from SID_MID where MID = {mid}'
        self.cursor.execute(sql)
        return self.query_strip()

    def getUserAllFavorSheet(self, UID):
        """用户收藏所有歌单数据
            返回一个二维列表
            [[SID, SName]]"""

        selectstr = f"select SID, SName from V$_getUserAllFavorSheet where UID = '{UID}'"
        self.cursor.execute(selectstr)
        resultlst = self.query_strip()
        return resultlst

    def getMusicR(self):
        """获得音乐收藏排序"""
        sql = 'select * from V$_getMusicData A left join  (select MID,count(*) n from SID_MID group by MID) as B on ' \
              'A.MID = B.MID order by n desc '
        self.cursor.execute(sql)
        return [i[:-2] for i in self.query_strip()]

    def createSheet(self, UID):
        """新建一个歌单
            返回成功与否"""

        # 获取用户名称
        selectstr = f"select UName from UserInfo where UID = {UID}"
        self.cursor.execute(selectstr)
        UName = self.query_strip()[0][0]
        print(UName)

        # 获取歌单所有名称
        allSheetSelect = f"select SID, SName from V$_getUserAllCreateSheet where UID = '{UID}'"
        self.cursor.execute(allSheetSelect)
        allSheet = self.query_strip()
        sheetNameList = []
        for sheet in allSheet:
            sheetNameList.append(sheet[1])
        print(sheetNameList)

        # 判断歌单数量是否超过限制
        if len(sheetNameList) > 9:
            return False
        else:
            # 若小于10 则创建一个新歌单
            if len(sheetNameList) > 0:
                for i in range(len(sheetNameList)):
                    if f"{UName}的歌单{i}" not in sheetNameList:
                        insertstr = f"insert into Sheet values ('{UName}的歌单{i}','{UName}创建的的歌单{i}',0)"
                        self.cursor.execute(insertstr)
                        self.conn.commit()

                        selectstr = f"select SID from Sheet where SName = '{UName}的歌单{i}'"
                        self.cursor.execute(selectstr)
                        SID = self.query_strip()[0][0]
                        # print(SID)

                        # 调用存储过程
                        self.cursor.callproc('Insert_USC', (UID, SID))
                        self.conn.commit()
            # 无歌单时创建一个厉害的歌单
            elif len(sheetNameList) == 0:
                insertstr = f"insert into Sheet values ('{UName}的主歌单','{UName}的歌单',0)"
                self.cursor.execute(insertstr)
                self.conn.commit()

                selectstr = f"select SID from Sheet where SName = '{UName}的主歌单'"
                self.cursor.execute(selectstr)
                SID = self.query_strip()[0][0]
                # print(SID)

                # 调用存储过程
                self.cursor.callproc('Insert_USC', (UID, SID))
                self.conn.commit()

            return True

    def updateSheetInfo(self, SID, SIntro):
        """更新歌单数据"""
        updatestr = f"update Sheet set SIntro = '{SIntro}'  where SID = {SID}"
        self.cursor.execute(updatestr)
        self.conn.commit()

    def deleteSheet(self, SID):
        """删除歌单"""
        deletestr = f'delete from Sheet where SID = {SID}'
        self.cursor.execute(deletestr)
        self.conn.commit()

    def unFavorSheet(self, UID, SID):
        """删除收藏歌单"""
        deletestr = f"delete from UID_SID_Favor where UID = {UID} and SID = {SID}"
        self.cursor.execute(deletestr)
        self.conn.commit()


if __name__ == "__main__":
    D = DataBase("127.0.0.1", "sa", "5151", "MMS")
    print(D.login("14589845", "SDJF1234"))
    print(D.get_user_info(1))
    print(D.get_all_user_label())
    print(D.getPlaylistSheetData(1))
    print(D.getPlaylistMusicData(1))
    print(D.getSearchUser("红茶honer"))
    print(D.getSearchMusic("月亮"))
    print(D.getUserAllCreateSheet(2))
    # print(D.createSheet(11))
    print(D.updateSheetInfo(1, 'test'))
    print(D.getMusicR())
    # print(D.login("14589845", "SDJF1234"))
    # print(D.get_user_info(1))
    # print(D.get_all_user_label())
    # print(D.getPlaylistSheetData(1))
    # print(D.getPlaylistMusicData(1))
    # print(D.getSearchUser("红茶honer"))
    # print(D.getSearchMusic("月亮"))
    # print(D.getUserAllCreateSheet(2))
    # # print(D.createSheet(11))
    # print(D.updateSheetInfo(1, 'test'))
    print(D.getUserRecommendSheet(1))
