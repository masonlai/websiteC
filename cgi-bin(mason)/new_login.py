#!C:\Users\sum\AppData\Local\Programs\Python\Python37-32\python.exe

import cgi
import sys

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers
print("<TITLE>Login page</TITLE>")
print(
"""<html lang="en" >

<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  <title>Login Form</title>

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
    .container {
      position: relative;
      z-index: 1;
      max-width: 300px;
      margin: 0 auto;
    }
    .container:before, .container:after {
      content: "";
      display: block;
      clear: both;
    }
    .container .info {
      margin: 50px auto;
      text-align: center;
    }
    .container .info h1 {
      margin: 0 0 15px;
      padding: 0;
      font-size: 36px;
      font-weight: 300;
      color: #1a1a1a;
    }
    .container .info span {
      color: #4d4d4d;
      font-size: 12px;
    }
    .container .info span a {
      color: #000000;
      text-decoration: none;
    }
    .container .info span .fa {
      color: #EF3B3A;
    }
    body {
      background: #FFFFFF; 
      font-family: "monospace", sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;      
    }  
  
  
</style>

  
</head>

<body>

  <div class="login-page">
  <div class="form">
    <form class="register-form" action="new_signup_func.py">
      <font>user name</font>
      <input type="text" name="su_username" required>
      <font>passwork</font>
      <input type="password" name="su_passwork" required>
      <font>full Name</font>
      <input type="text" name="full_name" required>
      <font>HKID</font>
      <input type="text" name="hkid">
      <font>email address</font>
      <input type="text" name="email_address"  required>
      <font>address</font>
      <input type="text" name="address">
      <font>phone numbers</font>
      <input type="text" name="phone_numbers" required>

      <button>create</button>
      <p class="message">Already registered? <a href="#">Sign In</a></p>
    </form>


    <form class="login-form" action="new_login_func.py" method="post">
      <input type="text" placeholder="username"/ name="login_username" required>
      <input type="password" placeholder="password"/ name="login_password" required>
      <button>login</button>
      <p class="message">Not registered? <a href="#">Create an account</a></p>
    </form>
  </div>
</div>
  <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

  

    <script>
      $('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});
</script>

</body>

</html>""")
