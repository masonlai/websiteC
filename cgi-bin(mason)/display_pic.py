import pymysql
from PIL import Image
from io import BytesIO
import base64, binascii

db = pymysql.connect("localhost",'root','','wsd')

cursor = db.cursor()

sql = """select picture from leaking_case
where issue_no = 102"""

try:
   cursor.execute(sql)
   db.commit()
   
except:
    print('error')
    db.rollback()
    
data_list = cursor.fetchone()
   
db.close()

bytes_pic = str.encode(data_list[0])

im = Image.open(BytesIO(base64.b64decode(bytes_pic)))

im.show()
