#!C:\Users\user\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi, cgitb
from class_pymysql import *
cgitb.enable()
form = cgi.FieldStorage()
print('''
<html>
<body>
<form method=post action='new_delet.py'>
issue no: <input type='text' name='issueno'></input>
delet: <input type='text' name='delet'></input>
<input type='submit' name='' value='comfirm'></input>
</form>
''')

connect = cgi_to_db()
connect.Connect_to_db()
    
if form.getvalue('delet') != None:
    try:
        sqll = ("""DELETE FROM `leaking_case` WHERE `leaking_case`.`issueNo` = '"""+form.getvalue('issueno')+"""'""")
        c = connect.Non_select(sqll)
    except:
        print('''gfdgsdg''')
    
print('''</body></html>''')
