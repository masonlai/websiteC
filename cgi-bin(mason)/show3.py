#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import time
import cgi
from PIL import Image
from io import BytesIO
import base64
import pymysql
import cgitb
from class_pymysql import *

f = open('C:/Windows/Temp/loginfile.dat')
user =f.read()

html5top='''
<!-- {fname} -->
<!DOCTYPE html>
<html>
 <head>
  <title>{title}</title>
 </head>
 <body>
  <h1>{header}</h1>
'''
html5bottom='''
 </body>
</html>
'''
tableHeader='''
<table border=1>
<tr><th>issue no</th><th>HKID</th><th>address</th><th>description</th><th>staff_ID</th><th>state</th><th>submit time</th></tr>
'''

form = cgi.FieldStorage()

if 'searchBy' in form:
    searchBy = form[ 'searchBy' ].value
else:
    searchBy = 'issueNo'
    
if 'searchKey' in form:  
    searchKey = form.getvalue('searchKey')
else:
    searchKey = ''

print (html5top.format(fname='hand2.py',title='searching',header='Searching Table'))

connect = cgi_to_db()
connect.Connect_to_db()


print('</table>')
print('<hr>')

print (time.ctime( time.time() ))

print ('''<br><br>
      <form method = 'post' action = '/cgi-bin/show3.py'>
      Search By:<br /><br>''')

sql = ('SELECT * from leaking_case where 1')
cname = connect.select_func2(sql)

for field in cname:
    print ('''<input type = 'radio' name = 'searchBy'
      value = '%s' />''' % field[ 0 ])
    print (field[ 0 ])
    print ("<br />")

print ('''<br />Search Key:<br />
      <input type = 'text' name = 'searchKey'
      value = '' />
      <br /><br />\n<input type = 'submit' value = 'Search' />
      </form><br><br>''')

print(tableHeader)

sqll = ('SELECT * from leaking_case WHERE %s  LIKE \'%s\' and %s  = \'%s\' and %s  = \'%s\'' %
                   ( searchBy, searchKey, 'state', 'Finish','staffID', str(user)))
c = connect.select_func(sqll)
for e in c:
    print ('<tr><td>'+str(e[0])+'</td>'+
                       '<td>'+e[1]+'</td>'+
                       '<td>'+e[2]+'</td>'+
                       '<td>'+e[3]+'</td>'+
                        '<td>'+str(e[4])+'</td>'+
                       '<td>'+e[5]+'</td>'+
                       '<td>'+str(e[6])+'</td></tr>')


print (html5bottom)


