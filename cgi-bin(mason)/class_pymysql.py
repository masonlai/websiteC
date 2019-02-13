import pymysql
import tkinter as tk
from tkinter import messagebox

class cgi_to_db:

    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__pwd = ''
        self.__db = 'wsd'

    def set_host(self,x):
        return self.__host == x
    
    def set_user(self,x):
        return self.__user == x

    def set_pwd(self,x):
        return self.__pwd == x

    def set_db(self,x):
        return self.__db == x

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

class windows():

        def errorwindows(self,x,y):
                root = tk.Tk()
                root.geometry('350x150')
                root.title(x)
                label = tk.Label(root, text=y)
                label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
                button = tk.Button(root, text="Quit", command=lambda: root.destroy())
                button.pack(side="bottom", fill="none", expand=True)
                root.mainloop()

class temp():

    def __init__(self):
        self.__value = 0

    def setvalue(self,x):
        return self.__value == x

    def getvalue(self):
        return self.__value

class checking():

    def isrange(self,x,y,z):
        if len(x)<=y or len(x)>=z:
            return False

    def isint(self,x):
        try:
            if int(x):
                return True
        except:
            return False
    
    def ishkid(self,hkid):
        '''
        the algorithm to make sure the hk id correct
        '''
        
        global id0
        
        for i in range(0,7):
            globals()['id'+str(i)] = hkid[i]
            
        hkid0 = letter_to_int(id0)
        id0 = hkid0
        hkid0 = int(id0)*8
        hkid1 = int(id1)*7
        hkid2 = int(id2)*6
        hkid3 = int(id3)*5
        hkid4 = int(id4)*4
        hkid5 = int(id5)*3
        hkid6 = int(id6)*2
        sum = hkid0 + hkid1 + hkid2 + hkid3 + hkid4 + hkid5 + hkid6
        remainder = sum%11
        
        if remainder == 0:
            last_num = 0
            
        else:
            last_num = 11 - remainder
            
        if last_num == int(hkid[7]):
            return False

        else:
            return True
