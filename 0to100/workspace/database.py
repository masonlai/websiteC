import pymysql 

class Database:
    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__pwd = 'vai'
        self.__db = 'project'

    def get_host(self):
        return self.__host

    def get_user(self):
        return self.__user

    def get_pwd(self):
        return self.__pwd

    def get_db(self):
        return self.__db

    def Connect_to_db(self):
        self.connection = pymysql.Connection(host=self.get_host(),
                user=self.get_user(),password=self.get_pwd(),database=self.get_db())
        cursor = self.connection.cursor()
        return cursor

    def return_db(self):
        self.connection = pymysql.Connection(host=self.get_host(),
                user=self.get_user(),password=self.get_pwd(),database=self.get_db())
        db = self.connection
        return db

    def select_func(self,sql):

        cursor = self.Connect_to_db()
        cursor.execute(sql)
        resList = cursor.fetchall()
        self.connection.close()
        return resList

    def select_func2(self,sql):

        cursor = self.Connect_to_db()
        cursor.execute(sql)
        resList = cursor.description
        self.connection.close()
        return resList

    def Non_select(self,sql):
        cursor = self.Connect_to_db()
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def Roll_back(self):
        RB = self.return_db()
        RB.rollback()
        RB.close()


connect = Database()
connect.Connect_to_db()
run = connect.select_func( """SELECT * FROM `user` WHERE `id` = '1' """)
print(run[0][0])