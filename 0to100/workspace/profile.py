import functools, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

import sys
import pymysql
from PIL import Image
from io import BytesIO
import base64

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

bp = Blueprint('profile', __name__,url_prefix='/profile')

@bp.route('/profile_edit', methods=('GET', 'POST'))
def profile_edit():
    connect = Database()
    connect.Connect_to_db()
    if request.method == 'POST':
        nick_name = "'"+request.form['Nick_name']+"'"
        country = "'"+request.form['Country']+"'"
        company ="'"+request.form['Company']+"'"
        time_zone = "'"+request.form['Time_zone']+"'"
        status = "'"+request.form['Status']+"'"
        try:
            icon = request.files['file']
            try:
                gender = "'"+request.form['Gender']+"'"
                base64_pic = "'"+image_to_base64(request.files['image'])+"'"
            except:
                base64_pic = 'NULL'
        except:
            icon = 'NULL'

        if not nick_name:
            nick_name = 'NULL'
        elif not company:
            company = 'NULL'
        elif not status:
            status = 'NULL'

        run = connect.Non_select("""UPDATE `Profile` SET `nick_name` = %s, `gender` = %s, `country` = %s, 
                `company` = %s, `time_zone` = %s, `status` = %s, `icon` = %s WHERE `Profile`.`ID` = %s"""%(nick_name, gender, country, company, time_zone, status, icon, g.user['ID']))


        return(nick_name)

    return render_template('profile/profile_edit.html')

