#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import os
import cgi, cgitb
import urllib.request
import base64
from PIL import Image
from io import BytesIO
from class_pymysql import *

def error_handling():
    '''
    handle the wrong input
    if there are error return True
    else it will return False
    '''
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
            error_message = 'length of phone numbers should not be more or less than 8'
            return True
            
        elif len(form.getvalue('email')) > 50:
            error_message = 'length of email should not be more than 50'
            return True
            
        elif '@' not in form.getvalue('email'):
            error_message = 'invalid email'
            return True
        
        elif len(form.getvalue('description')) >10000:
            error_message = 'length of description should not be more than 10000'
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
    '''
    the algorithm to make sure the hk id correct
    '''
    
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
    '''
    convert letter to a int number
    to support hkid_checking running the algorithm
    '''
    
    try:
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        return alphabet.index(letter) + 1
    
    except:
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return alphabet.index(letter) + 1

def image_to_base64(image_path):
    '''
    convert image to base64.
    It is beacuse database save picture in string form
    '''
    img = Image.open(image_path).convert('RGB')
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

cgitb.enable()# enable debugging(Trackback)

print("Content-type:text/html\r\n\r\n")

print()

form = cgi.FieldStorage()

if error_handling() == False:
    HTML = '''
    <div style="top:20px;left:400px;position:absolute;">Name:</div>
    <div style="top:40px;left:400px;position:absolute;">HKID:</div>
    <div style="top:60px;left:400px;position:absolute;">Phone numbers:</div>
    <div style="top:80px;left:400px;position:absolute;">Email:</div>
    <div style="top:100px;left:400px;position:absolute;">Address of leaking:</div>
    <div style="top:120px;left:400px;position:absolute;">description:</div>

    <div style="top:20px;left:550px;position:absolute;">'''+form.getvalue('name')+'''</div>
    <div style="top:40px;left:550px;position:absolute;">'''+form.getvalue('hkid')+'''</div>
    <div style="top:60px;left:550px;position:absolute;">'''+form.getvalue('phone_num')+'''</div>
    <div style="top:80px;left:550px;position:absolute;">'''+form.getvalue('email')+'''</div>
    <div style="top:100px;left:550px;position:absolute;">'''+form.getvalue('address')+'''</div>
    <div style="top:120px;left:550px;position:absolute;">'''+form.getvalue('description')+'''</div>
    '''
    HTML2 = '''
    <div style="top:160px;left:475px;position:absolute;">
    <button onclick="myFunction()">yes</button></div>
    
    <script>
    function myFunction() {
        alert("record was inserted into database successfully!");
    }
    </script>
    '''
    
    if "file" in form:
        form_file = form['file']
        # form_file is now a file object in python
        if form_file.filename:
    
            with open(form_file.filename, 'wb') as fout:
                # read the file in chunks as long as there is data
                while True:
                    chunk = form_file.file.read(10000000)
                    if not chunk:
                        break
                    # write the file content on a file in cgi-bin
                    fout.write(chunk)
    
            base64_pic = image_to_base64(form_file.filename)

    connect = cgi_to_db()
    connect.Connect_to_db()
    
    sql = """INSERT INTO citizen(HKID,
         name, phone, email)
         VALUES ('"""+form.getvalue('hkid')+"""', '"""+form.getvalue('name')+"""'
         , '"""+form.getvalue('phone_num')+"""', '"""+form.getvalue('email')+"""' )"""
    
    try:
       connect.Non_select(sql)
       
    except:
        connect.Roll_back()
    
    try:
    #if user upload file ,the code below will work
        sql = '''INSERT INTO `leaking_case` 
        (`HKID`, `address`, `description`, `picture`)
         VALUES ("'''+form.getvalue('hkid')+'''", 
         "'''+form.getvalue('address')+'''",
         "'''+form.getvalue('description')+'''", "'''+bytes.decode(base64_pic)+'''")'''
        
        os.remove(form_file.filename) #remove the image file in cgi-bin
        HTML += '<div style="top:140px;left:400px;position:absolute;">there are image</div>'
    except:
        sql = """INSERT INTO leaking_case(HKID,
             address, description)
             VALUES ('"""+form.getvalue('hkid')+"""
             ','"""+form.getvalue('address')+"""','"""+form.getvalue('description')+"""')"""
    
    try:
        connect.Non_select(sql)
        
    except:
        connect.Roll_back()
    
else:
    HTML = """
    <div style="text-align:center;background-color:red;height:60px;line-height:60px">
    <font color="white">"""+error_message+"""</font></div>
    """
    HTML2 = ' '

print(HTML+HTML2)


