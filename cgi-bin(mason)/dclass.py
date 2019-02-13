import pymysql
import tkinter as tk
from tkinter import messagebox
import sys

class logindata():

        user = []

        def __init__(self):
                self.__username = {}

        def set(self,x):
                self.__username = x

        def get(self):
                print(self.__username)
                return self.__username

        def add(self,x):
                user.append(x)

        def drop(self,x):
                user.remove(x)

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

class readdata():
        
        def __init__(self):
                self.__connection = 0

        def setconnection(self,x):
                return self.__connection == x

        def getconnection(self):
                return self.__connection

        def connect(self):
                global connection

                try:
                        connection = pymysql.connect(user='root',
                                     password='',
                                     db='wsd', 
                                     cursorclass=pymysql.cursors.DictCursor)
                        return True
                except pymysql.err.OperationalError:
                        windows.errorwindows(self,'Error','can not connect the database')  
                except ConnectionRefusedError:
                        windows.errorwindows(self,'Error','can not connect the database')

        def showtable(self):

                connection = pymysql.connect(user='root',
                                     password='',
                                     db='wsd', 
                                     cursorclass=pymysql.cursors.DictCursor)

                tableHeader='''
                    <table border=1>
                    <tr><th>issue no</th><th>HKID</th><th>address</th><th>staff_ID</th><th>state</th><th>submit time</th></tr>
                        '''

                print(tableHeader)

                with connection.cursor() as cursor:
                    cursor.execute('SELECT * from leaking_case WHERE %s LIKE \'%s\'' %
                                   ( searchBy, searchKey ))
                    allFields = cursor.description
                    for e in cursor.fetchall():
                        print ('<tr><td>'+str(e['issue_no'])+'</td>'+
                               '<td>'+e['HKID']+'</td>'+
                               '<td>'+e['address']+'</td>'+
                                '<td>'+str(e['staff_ID'])+'</td>'+
                               '<td>'+e['state']+'</td>'+
                               '<td>'+e['state']+'</td></tr>')

                print('</table>')

class errorhandling():

        error_message = str

        def isint(self):
                try:
                    int(self)
                    return True
                except ValueError:
                    return False

        def chkid(self) :
                
                if len(form.getvalue('hkid')) != 8 or self.hkid_checking(form.getvalue('hkid')):
                        return True
                else:
                        self.error_message = 'invalid hkid: '+form.getvalue('hkid')

        def saddress(self):
                pass

        def cissueno(self):
                pass

        def ctime(self):
                pass

        def error_handling(self):
            
            try :

                if len(form.getvalue('hkid')) != 8 or self.hkid_checking(form.getvalue('hkid')):
                    self.error_message = 'invalid hkid: '+form.getvalue('hkid')
                    return False

                elif len(form.getvalue('name')) > 20:
                    self.error_message = 'length of name should not be more than 20'
                    return False

                elif len(form.getvalue('phone_num')) != 8 and self.isint(form.getvalue('phone_num')):
                    self.error_message = 'length of phone numbers should not be more than 8'
                    return False

                elif len(form.getvalue('email')) > 50:
                    self.error_message = 'length of email should not be more than 50'
                    return False
                    
                elif '@' not in form.getvalue('email'):
                    self.error_message = 'invalid email: '+form.getvalue('email')
                    return False
                
                elif len(form.getvalue('address')) > 50:
                    self.error_message = 'length of Adress should not be more than 50'
                    return False
                    
            except:
                    
                return True

        def hkid_checking(self,hkid) :
            global id0
            
            for i in range(0,7):
                globals()['id'+str(i)] = hkid[i]
                
            hkid0 = self.letter_to_int(id0)
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

        def letter_to_int(self,letter):
            
            try:
                alphabet = list('abcdefghijklmnopqrstuvwxyz')
                return alphabet.index(letter) + 1
            
            except:
                alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                return alphabet.index(letter) + 1

class content():

        def staffcontent(self):

                print('Staff: '+form.getvalue('username'))

                print("<h3>Tool</h3>")
                print('<a href="show1.py">Not handling case</a><br>')
                print('<a href="show2.py">Handling case</a><br>')
                print('<a href="show3.py">Finished case</a><br>')
