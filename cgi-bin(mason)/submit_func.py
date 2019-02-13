#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi
import sys

def error_handling():
    global error_message
    
    try :
        int(form.getvalue('phone_num'))

        if len(form.getvalue('hkid')) != 8 or hkid_checking(form.getvalue('hkid')) == True :
            error_message = 'invalid hkid'
            return True
            
        elif len(form.getvalue('name')) > 20:
            error_message = 'length of name should not be more than 20'
            return True
            
        elif len(form.getvalue('phone_num')) != 8 :
            error_message = 'length of phone numbers should not be more than 8'
            return True
            
        elif len(form.getvalue('email')) > 50:
            error_message = 'length of email should not be more than 50'
            return True
            
        elif '@' not in form.getvalue('email'):
            error_message = 'invalid email'
            return True
        
        elif len(form.getvalue('address')) > 50:
            error_message = 'length of Adress should not be more than 50'
            return True
            
        else:
            return False
            
    except:
        error_message = 'invail phone numbers'
        return True
    
def hkid_checking(hkid) :
    global id0
    
    for i in range(0,7):
        globals()['id'+str(i)] = hkid[i]
        
    hkid0 = letter_to_int(id0)
    id0 = hkid0
    hkid0 = int(id0)*8
    hkid1 = int(id1)*7
    hkid2 = int(id2)*6
    hkid3 = int(id3)*5
    hkid4 = int(id4)*4
    hkid5 = int(id5)*3
    hkid6 = int(id6)*2
    sum = hkid0 + hkid1 + hkid2 + hkid3 + hkid4 + hkid5 + hkid6
    remainder = sum%11
    
    if remainder == 0:
        last_num = 0
        
    else:
        last_num = 11 - remainder
        
    if last_num == int(hkid[7]):
        return False

    else:
        return True


def letter_to_int(letter):
    
    try:
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        return alphabet.index(letter) + 1
    
    except:
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return alphabet.index(letter) + 1


print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers
print("<TITLE>submit form</TITLE>")

form = cgi.FieldStorage()

if error_handling() == False:
    print('''
    <div style="top:20px;left:400px;position:absolute;">Name:</div>
    <div style="top:40px;left:400px;position:absolute;">HKID:</div>
    <div style="top:60px;left:400px;position:absolute;">Phone numbers:</div>
    <div style="top:80px;left:400px;position:absolute;">Email:</div>
    <div style="top:100px;left:400px;position:absolute;">Address of leaking:</div>
            ''')
    
    print('''
    <div style="top:20px;left:550px;position:absolute;">'''+form.getvalue('name')+'''</div>
    <div style="top:40px;left:550px;position:absolute;">'''+form.getvalue('hkid')+'''</div>
    <div style="top:60px;left:550px;position:absolute;">'''+form.getvalue('phone_num')+'''</div>
    <div style="top:80px;left:550px;position:absolute;">'''+form.getvalue('email')+'''</div>
    <div style="top:100px;left:550px;position:absolute;">'''+form.getvalue('address')+'''</div>
            ''')
    
    
    print('''
            <div style="top:120px;left:475px;position:absolute;">
            <button onclick="myFunction()">yes</button></div>
            
            <script>
            function myFunction() {
                alert("record was inserted into database successfully!");
            }
            </script>
            ''')
    
    import pymysql
    
    db = pymysql.connect("localhost",'root','','wsd')
    
    cursor = db.cursor()
    
    sql = """INSERT INTO citizen(HKID,
         name, phone, email)
         VALUES ('"""+form.getvalue('hkid')+"""', '"""+form.getvalue('name')+"""'
         , '"""+form.getvalue('phone_num')+"""', '"""+form.getvalue('email')+"""' )"""
    
    try:
       cursor.execute(sql)
       db.commit()
       
    except:
       db.rollback()
       
    sql = """INSERT INTO leaking_case(HKID,
         address)
         VALUES ('"""+form.getvalue('hkid')+"""','"""+form.getvalue('address')+"""')"""
    
    try:
       cursor.execute(sql)
       db.commit()
       
    except:
       db.rollback()
    
    db.close()

else:
    print("""<div style="text-align:center;background-color:red;height:60px;line-height:60px">
    <font color="white">"""+error_message+"""</font></div>""")




