#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import pymysql, cgi, cgitb, os

cgitb.enable()

form = cgi.FieldStorage()

print("Content-Type: text/html")    
print()                             
print("<TITLE>Login page</TITLE>")

try:
    save_select = open('save.txt','r+')
    
    commentID = save_select.read()
    
    save_select.close()
    
    os.unlink(save_select.name)
    
    if form.getvalue('reply') != None:
        
        db = pymysql.connect("localhost",'root','','wsd')
        
        cursor = db.cursor()

        file = open('C:/Windows/Temp/loginfile.dat','r')
        
        login_id = file.read()

        sql = '''UPDATE `contact_us` SET `staffReply`= 
        "'''+form.getvalue('reply')+'''",  `staffID`= '''+login_id+''' WHERE 
        `commentId` = '''+commentID
        
        cursor.execute(sql)
        
        db.commit()
        
        db.close()
        
        print("""<div style="text-align:center;background-color:yellow;height:60px;line-height:60px">
            <font color="black">uploaded successfully</font></div>
            <a href='http://localhost/cgi-bin/new_staff_reply.py'>back</a>""")
        
    else:
        print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
        <font color="white">there are nothing was uploaded</font></div>
        <a href='http://localhost/cgi-bin/new_staff_reply.py'>back</a>""")
except:
    print('''<div style="text-align:center;background-color:red;height:60px;line-height:60px">
    <font color="white">you should select comment to reply</font></div>
    <a href='http://localhost/cgi-bin/new_staff_reply.py'>back</a>''')

