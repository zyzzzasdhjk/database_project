import pymssql


# server默认为127.0.0.1，如果打开了TCP动态端口的需要加上端口号，如'127.0.0.1:1433'
# user默认为sa
# password为自己设置的密码
# database为数据库名字
# 可简化为conn = pymssql.connect(host='localhost', user='sa', password='123456', database='pubs')

class DataBase:
    def __init__(self, server, user, password, database):
        self.conn = pymssql.connect(server, user, password, database, charset='cp936')
        self.cursor = self.conn.cursor()

    def query_strip(self):
        """将查询结果转换成二维列表"""
        data = self.cursor.fetchall()
        return [[j.strip() for j in i] for i in data]

    # def query(self, table_name: str, name=None):
    #     if name is None:
    #         name = ['*']
    #     self.cursor.execute(f"select {'.'.join(name)} from {table_name}")
    #     return self.query_strip()

    # def join_query(self, table_name1, table_name2, join_method, join_name1, join_name2=None, name=None):
    #     if name is None:
    #         name = ['*']
    #     if join_name2 is None:
    #         join_name2 = join_name1
    #     self.cursor.execute(f"select {'.'.join(name)} from {table_name1} {join_method} {table_name2} on "
    #                         f"{table_name1}.{join_name1} = {table_name2}.{join_name2}")

    def register(self, account, password):
        """注册槽函数"""
        judgestr = f"select account from AP where account = '{account}'"
        self.cursor.execute(judgestr)
        judgelist = self.query_strip()
        # print(judgelist)
        if not judgelist:
            self.cursor.execute(f"insert into AP (account,password) values ('{account}','{password}')")
            self.conn.commit()

    def login(self, account, password):
        """登录槽函数"""
        judgestr = f"select account from AP where account = '{account}' and password = '{password}'"
        self.cursor.execute(judgestr)
        judgelist = self.query_strip()
        # print(judgelist)
        if judgelist:
            print("True")

    def select_music_playlist(self):
        sql = "select pid from"


if __name__ == "__main__":
    D = DataBase("127.0.0.1", "sa", "5151", "SPJ")
    # print(D.query("AP", ["account"]))
    # print(D.query("AP", ["password"]))
    D.login("1", 2)
