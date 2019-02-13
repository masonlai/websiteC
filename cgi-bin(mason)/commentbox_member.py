#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi, cgitb
from class_pymysql import *

cgitb.enable()

print("Content-type:text/html")

print()

form = cgi.FieldStorage()
try:

    file = open('C:/Windows/Temp/mloginfile.dat','r')
    
    login_id = file.read()
    
    connect = cgi_to_db()
    connect.Connect_to_db()
    
    run = connect.Non_select( """INSERT INTO contact_us(userName,
         userComment)
         VALUES ('"""+login_id+"""', '"""+form.getvalue('comment')+"""')""")
    

except TypeError:
    pass
    

HTML='''<html>
<body>
<form action="commentbox_member.py">
<P><font>what is your comment:</font></P>
<textarea rows="8" cols="60" name="comment"></textarea>
<p></p>
<button type="submit" class="signupbtn" onclick="myFunction()">submit</button>
</form>
<script>
function myFunction() {
    alert("thanks for your comment!");
}
</script>

</body>
</html>'''

print(HTML)
