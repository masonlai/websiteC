#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import os
import cgi, cgitb
import urllib.request
import base64
from PIL import Image
from io import BytesIO
from class_pymysql import *

inFileData = None

cgitb.enable() # enable debugging(Trackback)

print("Content-type:text/html\r\n\r\n")# print content type
print()
        
form = cgi.FieldStorage()

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

try:
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
        
    HTML = '<div style="top:100px;left:400px;position:absolute;">upload successfully</div>'
        
    file = open('C:/Windows/Temp/mloginfile.dat','r')
    
    login_id = file.read()
    
    connect = cgi_to_db()
    connect.Connect_to_db()
    
    data = connect.select_func("""SELECT HKID from 
                    member where userName = '"""+login_id+"""'""")
    
    try:
    #if user upload file ,the code below will work
        sql = '''INSERT INTO `leaking_case` 
        (`HKID`, `address`, `description`, `picture`)
         VALUES ("'''+str(data[0][0])+'''", 
         "'''+form.getvalue('address')+'''",
         "'''+form.getvalue('description')+'''", "'''+bytes.decode(base64_pic)+'''")'''
        
        os.remove(form_file.filename) #remove the image file in cgi-bin
        HTML += '<div style="top:140px;left:400px;position:absolute;">there are image</div>'
    except:
        sql = """INSERT INTO leaking_case(HKID,
             address, description)
             VALUES ('"""+str(data[0][0])+"""
             ','"""+form.getvalue('address')+"""','"""+form.getvalue('description')+"""')"""
    
    try:
       connect.Non_select(sql)
       
    except:
        connect.Roll_back()
        

except:
    HTML = """
    <html>
    <head>
    <title></title>
    </head>
    <body>
    <form action="member_submit.py" method="POST" enctype="multipart/form-data" style="border:1px solid #ccc">
      <div class="container">
        <h1>Submit form</h1>
        <p>Please fill in this form to submit your problem.</p>
        
        <hr>
    
        <font>description:</font>
        <p>
        
        <textarea rows="8" cols="60" name="description" required></textarea>
        
        <p>
        
        <label for="address"><b>Address of leaking</b></label>
        <input type="text" placeholder="Enter Address" name="address" required>
    
        <p>By submiting a form you agree to our 
        <a href="/privacy.html" style="color:dodgerblue">Terms & Privacy</a>.</p>
    
        <div class="clearfix">
          <button type="reset" class="cancelbtn">Cancel</button>
          <button type="submit" class="signupbtn">Submit</button>
        </div>
        
        <hr>
        
        <b>upload picture:</b>
    
        <input type="file" name="file" onchange="readURL(this)" targetID="preview" accept="image/gif, image/jpeg, image/png"/ >
    
        <p>
        
        <b>accept jpg and png</b>
        
        <hr>
    
        <b>Preview:</b>
        
        <p>
    
        <img id="preview" src="#" " height="200" width="300"/>
    
      </div>
    </form>
    </body>
    </html>
    
    <script>
    
    function readURL(input){
    
      if(input.files && input.files[0]){
    
        var imageTagID = input.getAttribute("targetID");
    
        var reader = new FileReader();
    
        reader.onload = function (e) {
    
           var img = document.getElementById(imageTagID);
    
           img.setAttribute("src", e.target.result)
    
        }
    
        reader.readAsDataURL(input.files[0]);
    
      }
    
    }
    
    </script>
    """

print(HTML)
