#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import cgi, cgitb
from class_pymysql import *

cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html")    
print()                             
print("<TITLE>comment page</TITLE>")

file = open('C:/Windows/Temp/mloginfile.dat','r')

login_id = file.read()

connect = cgi_to_db()

data = connect.select_func("""SELECT commentId from 
                contact_us where userName = '"""+login_id+"""'""")

select_form_part1 = '''<form action="new_comment_member.py">
<font>selct the comment:</font><p>
<select name='selection' size=7>'''

for i in range(0,len(data)):
    select_form_part1 += '<option value='+str(data[i][0])+'''>comment_ID:
    '''+str(data[i][0])

select_form_part2 = '''</select>'''
    
display_area=' '

button = ('''<p><button type="submit" class="signupbtn">select</button>
</form><hr>''')

staff_reply = ('&nbsp'*55+'<font>The reply form staff:</font><p>'+'&nbsp'*60+'''<textarea 
rows="8" cols="60" name="comment"></textarea>''')

if form.getvalue('selection') != None:
    
    connect = cgi_to_db()
    connect.Connect_to_db()

    data2 = connect.select_func("""SELECT userComment, staffReply from 
                    contact_us where commentId = '"""+form.getvalue('selection')+"""'""")
    
    save_select = open('save.txt','w')
    
    save_select.write(form.getvalue('selection'))
    
    save_select.close()

    try:
        display_area = '&nbsp'*30+'''<textarea rows="8" cols="60" 
         name="comment">'''+str(data2[0][0])+'</textarea>'
         
        staff_reply = ('&nbsp'*55+'<font>The reply from staff:</font><p>'+'&nbsp'*60+'''
        <textarea rows="8" cols="60" 
        name="comment">'''+str(data2[0][1])+'''</textarea>''')

    except:
        display_area = '&nbsp'*30+'''<textarea rows="8" cols="60" 
         name="comment">'</textarea>'''
     
else:
    display_area = '&nbsp'*30+'<textarea rows="8" cols="60" name="comment"></textarea>'
    
print(select_form_part1 + select_form_part2 + display_area + button + staff_reply)
