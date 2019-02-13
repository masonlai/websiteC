#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import os
import cgi, cgitb
import pymysql
from class_pymysql import *

cgitb.enable()

def get_exsit_username():
    
    connect = cgi_to_db()
        
    data = connect.select_func("""SELECT userName from member where userName = '"""+form.getvalue('su_username')+"""'""")
    
    return data[0][0]

def error_handling():
    '''
    handle the wrong input
    if there are error return True
    else it will return False
    '''
    global error_message
    
    try :
        int(form.getvalue('phone_numbers'))

        if len(form.getvalue('hkid')) != 8 or hkid_checking(form.getvalue('hkid')) == True :
            error_message = 'invalid hkid'
            return True
            
        elif len(form.getvalue('su_username')) > 30:
            error_message = 'length of username should not be more than 30'
            return True
        
        elif len(form.getvalue('su_passwork')) > 30:
            error_message = 'length of passwork should not be more than 30'
            return True
        
        elif len(form.getvalue('full_name')) > 30:
            error_message = 'length of name should not be more than 30'
            return True
            
        elif len(form.getvalue('phone_numbers')) != 8 :
            error_message = 'length of phone numbers should not be more or less than 8'
            return True
            
        elif len(form.getvalue('email_address')) > 50:
            error_message = 'length of email should not be more than 50'
            return True
            
        elif '@' not in form.getvalue('email_address'):
            error_message = 'invalid email'
            return True
        
        elif len(form.getvalue('address')) > 50:
            error_message = 'length of Adress should not be more than 50'
            return True
            
        else:
            try:
                if form.getvalue('su_username') == get_exsit_username():
                    error_message = 'It is exist user name'
                    return True
                else:
                    return False
            except:
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
    
    
print("Content-Type: text/html")

print()

form = cgi.FieldStorage()

if error_handling() == False:
    HTML = '''
    <div style="top:20px;left:550px;position:absolute;">'''+form.getvalue('su_username')+'''</div>
    <div style="top:40px;left:550px;position:absolute;">'''+form.getvalue('su_passwork')+'''</div>
    <div style="top:60px;left:550px;position:absolute;">'''+form.getvalue('full_name')+'''</div>
    <div style="top:80px;left:550px;position:absolute;">'''+form.getvalue('hkid')+'''</div>
    <div style="top:100px;left:550px;position:absolute;">'''+form.getvalue('email_address')+'''</div>
    <div style="top:120px;left:550px;position:absolute;">'''+form.getvalue('address')+'''</div>
    <div style="top:140px;left:550px;position:absolute;">'''+form.getvalue('su_username')+'''</div>
'''

    connect = cgi_to_db()
    
    sql = ("""INSERT INTO member(userName,
         password, fullName, HKID, emailAddress, address, phoneNumbers)
         VALUES ('"""+form.getvalue('su_username')+"""', '"""+form.getvalue('su_passwork')+"""'
         , '"""+form.getvalue('full_name')+"""', '"""+form.getvalue('hkid')+"""' 
         , '"""+form.getvalue('email_address')+"""', '"""+form.getvalue('address')+"""'
         , '"""+form.getvalue('phone_numbers')+"""')""")
    
    try:
        connect.Non_select(sql)
        
    except:
        connect.Roll_back()

    
else:
    HTML = """
    <div style="text-align:center;background-color:red;height:60px;line-height:60px">
    <font color="white">"""+error_message+"""</font></div>
    """

print(HTML)
