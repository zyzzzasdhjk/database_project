import pymssql


# server默认为127.0.0.1，如果打开了TCP动态端口的需要加上端口号，如'127.0.0.1:1433'
# user默认为sa
# password为自己设置的密码
# database为数据库名字
# 可简化为conn = pymssql.connect(host='localhost', user='sa', password='123456', database='pubs')

class DataBase():
    def __init__(self, server, user, password, database, charset='cp936'):
        self.conn = pymssql.connect(server, user, password, database, charset='cp936')
        self.cursor = self.conn.cursor()

    def query_strip(self):
        data = self.cursor.fetchall()
        return [[j.strip() for j in i] for i in data]

    def query(self, table_name: str, name=None):
        if name is None:
            name = ['*']
        self.cursor.execute(f"select {'.'.join(name)} from {table_name}")
        self.query_strip()

    def join_query(self, table_name1, table_name2, join_method, join_name1, join_name2=None, name=None):
        if name is None:
            name = ['*']
        if join_name2 is None:
            join_name2 = join_name1
        self.cursor.execute(f"select {'.'.join(name)} from {table_name1} {join_method} {table_name2} on "
                            f"{table_name1}.{join_name1} = {table_name2}.{join_name2}")


if __name__ == "__main__":
    D = DataBase("127.0.0.1:1433", "sa", "5151", "py")
    print(D.query("S", ["Sno"]))