#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi, cgitb
from class_pymysql import *
cgitb.enable()
form = cgi.FieldStorage()
print('''
<html>
<body>
<form method=post action='new_update.py'>
issue no: <input type='text' name='issueno'></input>
address: <input type='text' name='address'></input>
description: <input type='text' name='description'></input>
<input type='submit' name='' value='comfirm'></input>
</form>
''')

connect = cgi_to_db()
connect.Connect_to_db()

if form.getvalue('address') != None:
    try:
        sqll = ("""update leaking_case set address='"""+form.getvalue('address')+"""' where issueNo ='"""+form.getvalue('issueno')+"""'""")
        c = connect.Non_select(sqll)
    except:
        print('''Error''')
    
if form.getvalue('description') != None:
    try:    
        sqll = ("""update leaking_case set description='"""+form.getvalue('description')+"""'where issueNo ='"""+form.getvalue('issueno')+"""'""")
        c = connect.Non_select(sqll)
    except:
        print('''Error''')

print('''</body></html>''')
