import functools, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

from workspace.default_icon import *

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


@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    connect = Database()
    connect.Connect_to_db()
    profile_info = connect.select_funcOne("""SELECT * FROM `Profile` WHERE `ID` = %s"""%g.user['ID'])
    bytes_icon = profile_info['icon']
    user_icon = base64.b64decode(bytes_icon)
    

    return render_template('profile/profile.html',profile_info=profile_info,user_icon=user_icon)

@bp.route('/profile_edit', methods=('GET', 'POST'))
def profile_edit():
    connect = Database()
    connect.Connect_to_db()
    global nick_name, country, company, time_zone, status, gender, icon
    if request.method == 'POST' and request.form['action'] == "SaveChanges":
        nick_name = request.form['Nick_name']
        country = request.form['Country']
        company =request.form['Company']
        time_zone = request.form['Time_zone']
        status = request.form['Status']
        gender = request.form['Gender']
        try:
            icon = request.files['file']
            base64_pic = image_to_base64(icon)
            icon = bytes.decode(base64_pic)
        except:
            icon = 'NULL'


        if not nick_name:
            nick_name = 'No_show'
        if not company:
            company = 'No_show'
        if not status:
            status = 'No_show'

        run = connect.Non_select("""UPDATE `Profile` SET `nick_name` = '%s', `gender` = '%s', `country` = '%s', 
            `company` = '%s', `time_zone` = '%s', `status` = '%s', 
            `icon` = '%s' WHERE `Profile`.`ID` = %s"""%(nick_name,gender,country,company,time_zone,status,icon,g.user['ID']))
        return(nick_name)
    elif request.method == 'POST' and request.form['action'] == "crop":
        return render_template('profile/crop.html')
    else:
        return render_template('profile/profile_edit.html')

@bp.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filenames = avatars.crop_avatar(session['raw_filename'], x, y, w, h)
        url_s = url_for('get_avatar', filename=filenames[0])
        url_m = url_for('get_avatar', filename=filenames[1])
        url_l = url_for('get_avatar', filename=filenames[2])
        return render_template('done.html', url_s=url_s, url_m=url_m, url_l=url_l)
    return render_template('profile/profile_edit.html')
