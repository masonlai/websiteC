#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import time
import cgi
import pymysql

html5bottom='''
 </body>
</html>
'''

form = cgi.FieldStorage()

print ('''
<html>
 <head>
 <style>
 
 .input{ width:300px;
     height:150px;
     padding: 0px;
     }
 
 </style>
 </head>
 <body>
''')
print ('''<br><br>
      <form method = 'post' action = '/cgi-bin/notice.py'>
      Notice:<br>''')
print('''<br><input type = 'text' name = 'notice'
      value = '' class="input">
      <br><input type = 'submit' value = 'set' />
      </form>''')

print (html5bottom)

f = open('notice.dat','w')
f.write(str(form.getvalue('notice')))
