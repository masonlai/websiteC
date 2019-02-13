#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi
import sys
import cgitb
import pymysql
import time
from class_pymysql import *

cgitb.enable()

f = open('notice.dat')
notice = f.read()

if notice != None:
    n= notice

html5bottom='''
 </body>
</html>
'''

print('''
<html>
 <head>
  <title>Login page</title>
  <style>
  body {
	font-family: Microsoft JhengHei;
}

.link {
	border = 0;
        margin: 0 auto;
        padding: 0;
	vertical-align: baseline;
	list-style-type: none;
	box-shadow: 0 3px 8px rgba(225, 225, 225, 1);

.sa{
	text-decoration:none;
	color: #588100;
}

.sa:link{
	text-decoration:none;
	color: #588100;
}

.sa:visited{
	text-decoration:none;
	color: #588100;
}

.sa:hover{
	text-decoration:none;
	color: #588100;
	background: #eeffe6;
}

  </style>
 </head>
 <body>
''')
form = cgi.FieldStorage()

import pymysql
    
connect = cgi_to_db()
connect.Connect_to_db()

data = connect.select_func("""SELECT staffID from staff where staffID = 
'"""+str(form.getvalue('login_username'))+"""'""")

data2 = connect.select_func("""SELECT password from staff where password = 
'"""+form.getvalue('login_password')+"""'""")

data3 = connect.select_func("""SELECT userName from member where userName = 
'"""+form.getvalue('login_username')+"""'""")

data4 = connect.select_func("""SELECT password from member where password = 
'"""+form.getvalue('login_password')+"""'""")

if len(data3) > 0:
    
    if len(data4) > 0:

        print("Login time is"+' '+time.ctime( time.time() ))
        print('<p>')
        print('<h1>Welcome</h1>')
        print(str(form.getvalue('login_username'))+'<br><br>')
        print('<div align="right"><a href="reminder_bar.py" class="sa">messages</a></div>')

        print("""<h2 class="link">Tool</h2><br>
                    <a href="hand22.py" class="sa">Search</a><br>
                    <a href="member_submit.py" class="sa">submit</a><br>
                    <a href="commentbox_member.py" class="sa">comment</a><br>
                    <a href="new_comment_member.py" class="sa">replied comment</a><br><br>
                    <h2 class="link"class="sa" >Notice</h2><br>""")
        print(n)


        mfile = open('C:/Windows/Temp/mloginfile.dat','w') 
        mfile.write(str(form.getvalue('login_username')))
        

    else:
        print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
        <font color="white">invalid password</font></div>""")
        
else:
    if len(data) > 0:
        if len(data2) > 0:

            print("Login time is"+' '+time.ctime( time.time() ))
            print('<p>')
            print('<h1>Welcome</h1>')
            print('<div align="right"><a href="remind_bar_staff.py" class="sa">messages</a></div>')
            print(str(form.getvalue('login_username'))+'<br><br>')
                
            print("""<h2 class="link">Tool</h2><br>
                    <a href="show1.py" class="sa">Leaking case</a><br>
                    <a href="show2.py" class="sa">Handling case</a><br>
                    <a href="show3.py" class="sa">Finished case</a><br>
                    <a href="new_staff_reply.py" class="sa">commony reply</a><br>
                    <h2 class="link">Notice</h2><br>""")
            print(n)

    
            file = open('C:/Windows/Temp/loginfile.dat','w') 
            file.write(str(form.getvalue('login_username')))
            
        else:
            print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
            <font color="white">invalid password</font></div>""")
            
    else:
        print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
        <font color="white">invalid username</font></div>""")
