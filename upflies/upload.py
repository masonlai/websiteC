import os
from flask import Flask, render_template, request
import sys
import pymysql
from PIL import Image
import base64
from io import BytesIO


class Database:
    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__pwd = 'vai'
        self.__db = 'project'

    def get_host(self):
        return self.__host

    def get_user(self):
        return self.__user

    def get_pwd(self):
        return self.__pwd

    def get_db(self):
        return self.__db

    def Connect_to_db(self):
        self.connection = pymysql.Connection(host=self.get_host(),
                user=self.get_user(),password=self.get_pwd(),database=self.get_db(),cursorclass=pymysql.cursors.DictCursor)
        cursor = self.connection.cursor()
        return cursor

    def select_funcOne(self,sql):

        cursor = self.Connect_to_db()
        cursor.execute(sql)
        resList = cursor.fetchone()
        self.connection.close()
        return resList

    def select_funcALL(self,sql):

        cursor = self.Connect_to_db()
        cursor.execute(sql)
        resList = cursor.fetchall()
        self.connection.close()
        return resList

    def Non_select(self,sql):
        cursor = self.Connect_to_db()
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def Roll_back(self):
        RB = self.return_db()
        RB.rollback()
        RB.close()


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


app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    connect = Database()
    connect.Connect_to_db()
    file = request.files['image']
    base64_pic = image_to_base64(file)
    connect.Non_select("""UPDATE `Profile` SET `nick_name` = '123321', `gender` = '123', `country` = '123123', `company` = '312No_show', 
        `time_zone` = '312', `status` = '213', `icon` = '"""+bytes.decode(base64_pic)+"""' WHERE `Profile`.`ID` = 9""")

    return base64_pic