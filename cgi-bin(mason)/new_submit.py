#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe
import cgi, cgitb, sys

inFileData = None

cgitb.enable() # enable debugging(Trackback)

print("Content-type:text/html\r\n\r\n")# print content type
print()

 
HTML = """
<html>
<head>

<style>
.barheader{
	border = 0;
        background: #006AB4;
	padding: 0 20px;
	word-spacing:5px;
}

a{
	text-decoration:none;
}

a:link {
　//設定還沒瀏覽過的連結樣式
	text-decoration:none;
	color: #fff;
}
a:visited {
　//設定已經瀏覽過的連結樣式
	text-decoration:none;
	color: white;
}
a:hover {
　//設定滑鼠移到連結上的樣式
	text-decoration:none;
	color: #d9ff66;
}
.sa{
	text-decoration: underline;
	color: #588100;
}

.sa:link{
	text-decoration: underline;
	color: #588100;
}

.sa:visited{
	text-decoration: underline;
	color: #588100;
}

.sa:hover{
	text-decoration: underline;
	color: #588100;
	background: #eeffe6;
}

    .login-page {
      width: 660px;
      padding: 8% 0 0;
      margin: auto;
    }
    .form {
      position: relative;
      z-index: 1;
      background: #A3D7FA;
      max-width: 360px;
      margin: 0 auto 100px;
      padding: 45px;
      text-align: left;
      box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
    }
    .form input {
      font-family: "monospace", sans-serif;
      outline: 0;
      background: #f2f2f2;
      width: 100%;
      border: 0;
      margin: 0 0 15px;
      padding: 15px;
      box-sizing: border-box;
      font-size: 14px;
    }
    .form button {
      font-family: "monospace", sans-serif;
      text-transform: uppercase;
      outline: 0;
      background: #59B8F8;
      width: 100%;
      border: 0;
      padding: 15px;
      color: #FFFFFF;
      font-size: 14px;
      -webkit-transition: all 0.3 ease;
      transition: all 0.3 ease;
      cursor: pointer;
    }
    .form button:hover,.form button:active,.form button:focus {
      background: #1D98EA;
    }
    .form .message {
      margin: 15px 0 0;
      color: #040404;
      font-size: 12px;
    }
    .form .message a {
      color: #59B8F8;
      text-decoration: none;
    }
    .form .register-form {
      display: none;
    }
    body {
      background: #FFFFFF; 
      font-family: "monospace", sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;      
    }  
  

ul { /* 取消ul預設的內縮及樣式 */
	border = 0;
        margin: 0 auto;
        padding: 0;
	vertical-align: baseline;
	list-style-type: none;
	box-shadow: 0 3px 8px rgba(225, 225, 225, 1);
    }

    ul.drop-down-menu {
	border = 0;
        display: table-cell;
        font-size: 15px;
        vertical-align: middle;
        text-align: center;
	list-style-type: none;
    }

    ul.drop-down-menu li {
	border = 0;
        position: relative;
        white-space: nowrap;
    }

    ul.drop-down-menu > li:last-child {

    }

    ul.drop-down-menu > li {
        float: left; /* 只有第一層是靠左對齊*/
    }

     ul.drop-down-menu a {
	color: #000000;
        display: block;
        padding: 0 30px;
        text-decoration: none;
        line-height: 40px;
    }
    ul.drop-down-menu a:hover { /* 滑鼠滑入按鈕變色*/
	color: #ffffff;
        background: #0e838d;
    }
    ul.drop-down-menu li:hover > a { /* 滑鼠移入次選單上層按鈕保持變色*/
   	 color:  #ffffff;
   	 background: #0e838d;
    }
  ul.drop-down-menu ul { /*隱藏次選單*/
        display: none;
    }

    ul.drop-down-menu li:hover > ul { /* 滑鼠滑入展開次選單*/
        display: block;
	color:  #000000;
   	background:#0e838d;
    }
  ul.drop-down-menu ul {
        border: 0;
        position: absolute;
        z-index: 99;
        left: -1px;
        top: 100%;
       min-width: 180px;
    }

    ul.drop-down-menu ul li {
   	background:#e6ffff;
    }

    ul.drop-down-menu ul li:last-child {
	border-bottom: none;
    }

    ul.drop-down-menu ul ul { /*第三層以後的選單出現位置與第二層不同*/
        z-index: 999;
        top: 10px;
        left: 90%;
    }
  
</style>

<title></title>
</head>
<body>

 <div>
<ul>
<li class="barheader">
<div align="right"><a href="/cgi-bin/new_login.py">Login</a></div>
</li>
<li>
<a href="https://www.wsd.gov.hk/tc/home/index.html" target="_blank"><img src="/wsd_logo.png"></a>
</li>
 <li><ul class="drop-down-menu">
        <li><a href="/index.html">Home</a>
        </li>
        <li><a href="/aboutus.html">About us</a>
        </li>
        <li><a href="/hand.html">Leaking Report and Inquire
		<ul>
		<li><a href="/cgi-bin/new_submit.py">Leaking Report</a>
		<li><a href="/cgi-bin/hand22.py">Inquire</a>
		</ul></a>
        </li>
        <li><a href="/sitemap.html">sitemap</a>
        </li>
    </li></ul>
</ul>
</div><br>

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
