#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import pymysql, cgi, cgitb
from class_pymysql import *

cgitb.enable()

f = open('C:/Windows/Temp/loginfile.dat')
user = f.read()

print("Content-Type: text/html")    
print()                             
print("<TITLE>Login page</TITLE>")

connect = cgi_to_db()
connect.Connect_to_db()

data = connect.select_func2("""SELECT commentId from contact_us where userName = '"""+user+"""'""")

try:
    print("""<div style="top:20px;left:1100px;position:absolute;">
    you have """+str(len(data))+"""message</div><br><br>""")
    print("""<div style="top:60px;left:1100px;position:absolute;">
    <input type ="button" onclick="history.back()" value="Back">
    </input></div>""")
    
except:
    print("""<div style="top:20px;left:1100px;position:absolute;">
    you have no message</div><br><br>""")
    print("""<div style="top:60px;left:1100px;position:absolute;">
        <input type ="button" onclick="history.back()" value="Back">
        </input></div>""")
