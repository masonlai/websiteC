#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi
import sys

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers
print("<TITLE>submit form</TITLE>")

form = cgi.FieldStorage()

print('''<form action="submit_func.py" style="border:1px solid #ccc">
  <div class="container">
    <h1>Submit form</h1>
    <p>Please fill in this form to submit your problem.</p>
    <hr>

    <label for="name"><b>Name</b></label>
    <input type="text" placeholder="Enter your full name" name="name" required>
    
    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>
    
    <label for="hkid"><b>HKID</b></label>
    <input type="text" placeholder="Enter your HKID whihout ()" name="hkid" required>
    
    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>

    <label for="phone_num"><b>Phone Numbers</b></label>
    <input type="text" placeholder="Enter your numbers" name="phone_num" required>

    <p>
    
    <label for="email"><b>Email</b></label>
    <input type="text" placeholder="Enter Email" name="email" required>
    
    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>
    
    <label for="address"><b>Address of leaking</b></label>
    <input type="text" placeholder="Enter Address" name="address" required>

    <p>By creating an account you agree to our 
    <a href="/privacy.html" style="color:dodgerblue">Terms & Privacy</a>.</p>

    <div class="clearfix">
      <button type="reset" class="cancelbtn">Cancel</button>
      <button type="submit" class="signupbtn">Submit</button>
      
    </div>
  </div>
</form>''')

print (html5bottom)

