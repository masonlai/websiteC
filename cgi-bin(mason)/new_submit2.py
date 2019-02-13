#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import cgi, cgitb, sys

inFileData = None

cgitb.enable() # enable debugging(Trackback)

print("Content-type:text/html\r\n\r\n")# print content type
print()

 
HTML = """
<html>
<head>
<title></title>
</head>
<body>
<form action="new_submit_func.py" method="POST" enctype="multipart/form-data" style="border:1px solid #ccc">
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
    
    <p></p>
    
    <font>description:</font>
    <p>
    
    <textarea rows="8" cols="60" name="description" required></textarea>

    <p>By submiting a form you agree to our 
    <a href="/privacy.html" style="color:dodgerblue">Terms & Privacy</a>.</p>

    <div class="clearfix">
      <button type="reset" class="cancelbtn">Cancel</button>
      <button type="submit" class="signupbtn" >Submit</button>
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
