#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import time
import cgi
import sys
import pymysql
import setting
from dclass import *

f = open('notice.dat')
notice = f.read()

if notice != None:
    n= notice

html5bottom='''
 </body>
</html>
'''

print('''
<!-- {fname} -->
<!DOCTYPE html>
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

.barheader{
	border = 0;
        background: #006AB4;
	padding: 0 20px;
	word-spacing:5px;
}

a{
	text-decoration:none;
}

a:link {
　//設定還沒瀏覽過的連結樣式
	text-decoration:none;
	color: #fff;
}
a:visited {
　//設定已經瀏覽過的連結樣式
	text-decoration:none;
	color: white;
}
a:hover {
　//設定滑鼠移到連結上的樣式
	text-decoration:none;
	color: #d9ff66;
}
.sa{
	text-decoration: underline;
	color: #588100;
}

.sa:link{
	text-decoration: underline;
	color: #588100;
}

.sa:visited{
	text-decoration: underline;
	color: #588100;
}

.sa:hover{
	text-decoration: underline;
	color: #588100;
	background: #eeffe6;
}

    .login-page {
      width: 660px;
      padding: 8% 0 0;
      margin: auto;
    }
    .form {
      position: relative;
      z-index: 1;
      background: #A3D7FA;
      max-width: 360px;
      margin: 0 auto 100px;
      padding: 45px;
      text-align: left;
      box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
    }
    .form input {
      font-family: "monospace", sans-serif;
      outline: 0;
      background: #f2f2f2;
      width: 100%;
      border: 0;
      margin: 0 0 15px;
      padding: 15px;
      box-sizing: border-box;
      font-size: 14px;
    }
    .form button {
      font-family: "monospace", sans-serif;
      text-transform: uppercase;
      outline: 0;
      background: #59B8F8;
      width: 100%;
      border: 0;
      padding: 15px;
      color: #FFFFFF;
      font-size: 14px;
      -webkit-transition: all 0.3 ease;
      transition: all 0.3 ease;
      cursor: pointer;
    }
    .form button:hover,.form button:active,.form button:focus {
      background: #1D98EA;
    }
    .form .message {
      margin: 15px 0 0;
      color: #040404;
      font-size: 12px;
    }
    .form .message a {
      color: #59B8F8;
      text-decoration: none;
    }
    .form .register-form {
      display: none;
    }
    .container {
      position: relative;
      z-index: 1;
      max-width: 300px;
      margin: 0 auto;
    }
    .container:before, .container:after {
      content: "";
      display: block;
      clear: both;
    }
    .container .info {
      margin: 50px auto;
      text-align: center;
    }
    .container .info h1 {
      margin: 0 0 15px;
      padding: 0;
      font-size: 36px;
      font-weight: 300;
      color: #1a1a1a;
    }
    .container .info span {
      color: #4d4d4d;
      font-size: 12px;
    }
    .container .info span a {
      color: #000000;
      text-decoration: none;
    }
    .container .info span .fa {
      color: #EF3B3A;
    }
    body {
      background: #FFFFFF; 
      font-family: "monospace", sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;      
    }  
  

ul { /* 取消ul預設的內縮及樣式 */
	border = 0;
        margin: 0 auto;
        padding: 0;
	vertical-align: baseline;
	list-style-type: none;
	box-shadow: 0 3px 8px rgba(225, 225, 225, 1);
    }

    ul.drop-down-menu {
	border = 0;
        display: table-cell;
        font-size: 15px;
        vertical-align: middle;
        text-align: center;
	list-style-type: none;
    }

    ul.drop-down-menu li {
	border = 0;
        position: relative;
        white-space: nowrap;
    }

    ul.drop-down-menu > li:last-child {

    }

    ul.drop-down-menu > li {
        float: left; /* 只有第一層是靠左對齊*/
    }

     ul.drop-down-menu a {
	color: #000000;
        display: block;
        padding: 0 30px;
        text-decoration: none;
        line-height: 40px;
    }
    ul.drop-down-menu a:hover { /* 滑鼠滑入按鈕變色*/
	color: #ffffff;
        background: #0e838d;
    }
    ul.drop-down-menu li:hover > a { /* 滑鼠移入次選單上層按鈕保持變色*/
   	 color:  #ffffff;
   	 background: #0e838d;
    }
  ul.drop-down-menu ul { /*隱藏次選單*/
        display: none;
    }

    ul.drop-down-menu li:hover > ul { /* 滑鼠滑入展開次選單*/
        display: block;
	color:  #000000;
   	background:#0e838d;
    }
  ul.drop-down-menu ul {
        border: 0;
        position: absolute;
        z-index: 99;
        left: -1px;
        top: 100%;
       min-width: 180px;
    }

    ul.drop-down-menu ul li {
   	background:#e6ffff;
    }

    ul.drop-down-menu ul li:last-child {
	border-bottom: none;
    }

    ul.drop-down-menu ul ul { /*第三層以後的選單出現位置與第二層不同*/
        z-index: 999;
        top: 10px;
        left: 90%;
    }
  
</style>
 </head>
 <body>

 <div>
<ul>
<li class="barheader">
<div align="right"><a href="\cgi-bin\new_login.py">Login</a></div>
</li>
<li>
<a href="https://www.wsd.gov.hk/tc/home/index.html" target="_blank"><img src="wsd_logo.png"></a>
</li>
 <li><ul class="drop-down-menu">
        <li><a href="index.html">Home</a>
        </li>
        <li><a href="aboutus.html">About us</a>
        </li>
        <li><a href="hand.html">Leaking Report and Inquire
		<ul>
		<li><a href="/cgi-bin/new_submit.py">Leaking Report</a>
		<li><a href="/cgi-bin/hand22.py">Inquire</a>
		</ul></a>
        </li>
        <li><a href="sitemap.html">sitemap</a>
        </li>
    </li></ul>
</ul>
</div><br>
''')

form = cgi.FieldStorage()

print("Login time is"+' '+time.ctime( time.time() ))
print('<p>')
print('<h1>Welcome</h1>')

db = pymysql.connect("localhost",'root','','wsd')

cursor = db.cursor()

cursor.execute("""SELECT staff_ID from staff where staff_ID = '"""+str(form.getvalue('username'))+"""'""")

data = cursor.fetchone()

cursor.execute("""SELECT password from staff where password = '"""+form.getvalue('password')+"""'""")

data2 = cursor.fetchone()

db.close()

user = form.getvalue('username')
print(user)
print()
if data != None:
    
    if data2 != None:

            print("""<h3 class="link">Tool</h3><br>
                    <a href="show1.py">Leaking case</a><br>
                    <a href="show2.py">Handling case</a><br>
                    <a href="show3.py">Finished case</a><br><br>
                    <h2 class="link">Notice</h2><br>""")
            print(n)
        
    else:
        print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
        <font color="white">invalid password</font></div>""")
        
else:
    print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
    <font color="white">invalid username</font></div>""")

print(html5bottom)

file = open('C:/Windows/Temp/loginfile.dat','w') 
file.write(str(form.getvalue('username')))
