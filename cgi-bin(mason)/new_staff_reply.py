#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import cgi, cgitb
from class_pymysql import *

cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html")    
print()                             
print("<TITLE>comment page</TITLE>")

connect = cgi_to_db()
connect.Connect_to_db()

data = connect.select_func("""SELECT commentId from 
                contact_us where staffReply = ''""")

select_form_part1 = '''<form action="new_staff_reply.py">
<font>selct the comment:</font><p>
<select name='selection' size=7>'''

for i in range(0,len(data)):
    select_form_part1 += '<option value='+str(data[i][0])+'''>comment_ID:
    '''+str(data[i][0])

select_form_part2 = '''</select>'''

display_area=' '

button = ('''<p><button type="submit" class="signupbtn">select</button>
</form><hr>''')

if form.getvalue('selection') != None:
    
    data2 = connect.select_func("""SELECT userComment from 
                    contact_us where commentId = '"""+form.getvalue('selection')+"""'""")
        
    save_select = open('save.txt','w')
    
    save_select.write(form.getvalue('selection'))
    
    save_select.close()
    
    display_area = '&nbsp'*30+'''<textarea rows="8" cols="60" 
     name="comment">'''+str(data2[0][0])+'</textarea>'
else:
    display_area = '&nbsp'*30+'<textarea rows="8" cols="60" name="comment"></textarea>'

if len(data) != 0:

    print(select_form_part1 + select_form_part2 + display_area + button)
    
    print("""<form action="new_staff_reply_func.py">
        <font>there are your reply for comment :</font><p>
        <textarea rows="8" cols="60" 
        name='reply'></textarea><p>
        <button type="submit" class="signupbtn" >submit</button></div>
        </form>""")
    
else:
    print('''<div style="text-align:center;background-color:red;height:60px;line-height:60px">
        <font color="white">you have no comment have to reply</font></div>''')

