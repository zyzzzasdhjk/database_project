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
            若满足账号密码需求，则返回True"""

        judgestr = f"select account from Account_Password where account = '{account}' and password = '{password}'"
        self.cursor.execute(judgestr)
        judgelist = self.query_strip()
        print(judgelist)
        if judgelist:
            return True
        else:
            return False

    def getPlaylistMusicData(self, SID):
        """从视图中获取歌单歌曲数据
            返回二维列表[[SID, MID, MName, MTime, MDate, MMName]]"""

        selectstr = f"select * from V$_getPlaylistMusicData where SID = {int(SID)}"
        self.cursor.execute(selectstr)
        MusicDatalist = self.query_strip()
        return MusicDatalist

    def getPlaylistSheetData(self, SID):
        """从表与视图中获取歌单数据
            返回一维列表[SID, SName, SIntro, SFavor, MusicNum]"""

        selectstr1 = f"select SID, SName,SIntro,SFavor from Sheet where SID = {int(SID)}"
        selectstr2 = f"select MusicNum from V$_getSheetMusicNum where SID = {int(SID)}"
        self.cursor.execute(selectstr1)
        SheetDatalist = self.query_strip()[0]
        self.cursor.execute(selectstr2)
        SheetDatalist = SheetDatalist + self.query_strip()[0]
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

        sql = f'select * from V$_getUserInformation where UID={uid}' # V$_getUserInformation
        self.cursor.execute(sql)
        # data = self.cursor.fetchall()
        l = self.query_strip()
        return l

    def change_user_info(self, uid, lst):
        sql = f"delete from UserInfo where uid = {uid}"

    def getSearchUser(self, searchstr):
        """搜索
            返回模糊匹配的二维列表"""
        pass

    def getSearchMusic(self, searchstr):
        """搜索
            返回模糊匹配的二维列表"""
        pass


if __name__ == "__main__":
    D = DataBase("127.0.0.1", "sa", "5151", "MMS")
    print(D.register("14589845", "SDJF1234"))
    print(D.get_user_info(1))
    print(D.get_all_user_label())
    print(D.getPlaylistSheetData(1))
    print(D.getPlaylistMusicData(1))
