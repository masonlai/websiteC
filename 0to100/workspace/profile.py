import functools, os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

import sys
import pymysql
from PIL import Image
from io import BytesIO
import base64
from flask_avatars import Avatars
import datetime
from workspace.login_app import login_required


avatars = Avatars()

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
@bp.route('/profile/<int:id>',defaults={'cl':1,'menu':'HomePage','order':'A'}, methods=('GET', 'POST'))
@bp.route('/profile/<int:id>/<menu>',defaults={'cl':1,'order':'A'}, methods=('GET', 'POST'))
@bp.route('/profile/<int:id>/<menu><int:cl><order>', methods=('GET', 'POST'))
def profile(id,cl,menu,order):
    connect = Database()
    connect.Connect_to_db()
    profile_info = connect.select_funcOne("""SELECT * FROM `Profile` WHERE `ID` ='%s'"""%id)
    user_icon = profile_info['icon']



    paginate =[]
    count = 0
    row = []
    if menu == 'collection':
        if order == 'B':
            collection =  connect.select_funcALL("""SELECT collection.`picture_ID` , \
                collection.timestamp , picture.picture ,picture.title FROM \
                `collection` JOIN picture ON collection.`picture_ID` = picture.ID WHERE\
                 collection.`collecter_ID`=%s ORDER BY collection.timestamp """%id)
        else:
            collection =  connect.select_funcALL("""SELECT collection.`picture_ID` , \
                collection.timestamp , picture.picture ,picture.title FROM \
                `collection` JOIN picture ON collection.`picture_ID` = picture.ID WHERE\
                 collection.`collecter_ID`=%s ORDER BY collection.timestamp DESC"""%id)
        count = len(collection)

        for i in range(0,len(collection),3):
            row.append(collection[i:i+3])

        for i in range(0,len(row),2):
            paginate.append(row[i:i+2])


    elif menu == 'Gallery' :


        if order == 'B':
            Gallery =  connect.select_funcALL("""SELECT `ID`,`title`,`picture`,\
                `timestamp`FROM `picture` WHERE `auth_ID`='%s' ORDER BY timestamp """%id)
        else:
            Gallery =  connect.select_funcALL("""SELECT `ID`,`title`,`picture`,\
                `timestamp`FROM `picture` WHERE `auth_ID`='%s' ORDER BY timestamp DESC"""%id)

        count = len(Gallery)

        for i in range(0,len(Gallery),3):
            row.append(Gallery[i:i+3])

        for i in range(0,len(row),2):
            paginate.append(row[i:i+2])


    elif menu == 'Follow':
        if order == 'B':
            following =  connect.select_funcALL("""select * from follow where follower = %s ORDER BY timestamp"""%id)
        else:
            following =  connect.select_funcALL("""select * from follow where follower = %s ORDER BY timestamp DESC"""%id)
        count = len(following)
        for i in range(len(following)):
            Gallery = connect.select_funcOne("""select COUNT(*) from picture where auth_ID = %s"""%following[i]['following'])
            follower = connect.select_funcOne("""select COUNT(*) from follow where following = %s"""%following[i]['following'])
            follow_name = connect.select_funcOne("""select nick_name from Profile where ID = %s"""%following[i]['following'])
            following[i]['gallery'] = Gallery['COUNT(*)']
            following[i]['followers'] = follower['COUNT(*)']
            following[i]['name'] = follow_name['nick_name']


        for i in range(0,len(following),9):
            paginate.append(following[i:i+9])



    else:
        menu = 'HomePage'

    check_follow='N'
    if not not g.user:
        follow = connect.select_funcOne("""select *from follow where following = %s and follower = %s"""%(id,g.user['ID']))
        if not follow:
            check_follow='N'
        else:
            check_follow='Y'


    if request.method == 'POST':
        backgroud = request.form['background']
        run = connect.Non_select("""UPDATE `Profile` SET `background` = '%s'
            WHERE `Profile`.`ID` = %s"""%(backgroud, g.user['ID']))
        profile_info = connect.select_funcOne("""SELECT * FROM `Profile` WHERE `ID` = %s"""%id)
        user_icon = profile_info['icon']
    joined = str(profile_info['joined_date'])[0:10]
    changed = str(profile_info['changed_date'])
    current_time = str(datetime.datetime.now())[0:19]
    if len(paginate)< (cl-1):
        cl = 1
    return render_template('profile/profile.html',id=id,int=int,profile_info=profile_info,len=len,\
        user_icon=user_icon, joined=joined,changed=changed,\
        menu=menu,current_time=current_time,paginate=paginate,cl=cl,count=count,row=row,order=order,check_follow=check_follow)

@bp.route('/profile_edit', methods=('GET', 'POST'))
@login_required
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
            icon = session['url_l'][9:]
            base64_pic = image_to_base64(icon)
            icon = bytes.decode(base64_pic)
        except:
            icon = 'default'

        if not nick_name:
            nick_name = 'No_show'
        if not company:
            company = 'No_show'
        if not status:
            status = 'No_show'

        run = connect.Non_select("""UPDATE `Profile` SET `nick_name` = '%s', `gender` = '%s', `country` = '%s', 
            `company` = '%s', `time_zone` = '%s', `status` = '%s', 
            `icon` = '%s' WHERE `Profile`.`ID` = %s"""%(nick_name,gender,country,company,time_zone,status,icon,g.user['ID']))
        return redirect(url_for('profile.profile',id=g.user['ID']))

    elif request.method == 'POST' and request.form['action'] == "crop":
        f = request.files.get('file')
        raw_filename = avatars.save_avatar(f)
        session['raw_filename'] = raw_filename  
        return redirect(url_for('profile.crop'))

    else:
        profile_info = connect.select_funcOne("""SELECT * FROM `Profile` WHERE `ID` = %s"""%g.user['ID'])
        user_icon = profile_info['icon']
        return render_template('profile/profile_edit.html',url_l=request.args.get('url_l'),crop=request.args.get('crop'),user_icon=user_icon,profile_info=profile_info)

@bp.route('/crop', methods=['GET', 'POST'])
@login_required
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filenames = avatars.crop_avatar(session['raw_filename'], x, y, w, h)
        url_l = url_for('profile.get_avatar', filename=filenames[2])
        crop='done'
        session['url_l']=url_l
        return redirect(url_for('profile.profile_edit',url_l=url_l,crop=crop))
    else:
        return render_template('profile/crop.html')

@bp.route('/avatars/<path:filename>')
@login_required
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)

@bp.route('/Myprofile', methods=['GET', 'POST'])
@login_required
def Myprofile():
    return redirect(url_for('profile.profile',id=g.user['ID']))


@bp.route('/follow<int:id>/<check_follow>', methods=['GET', 'POST'],defaults={'menu':'idc','cl':1,'order':'B'})
@bp.route('/follow/<int:id>/<menu><int:cl><order>/<check_follow>', methods=('GET', 'POST'))
@login_required
def follow(id,check_follow,menu,cl,order):
    connect = Database()
    connect.Connect_to_db()
    if check_follow == 'N':
        run = connect.Non_select("""INSERT INTO `follow` (`following`, `follower`,\
         `timestamp`) VALUES ('%s', '%s', CURRENT_TIMESTAMP)"""%(id,g.user['ID']))
        flash('Follow successful','success')
    elif check_follow =='F':
        run = connect.Non_select("""DELETE FROM `follow` where `following`=%s and `follower`=%s"""%(id,g.user['ID']))
        flash('Unfollow successful','warning')
        return redirect(url_for('profile.profile',id=g.user["ID"],menu='Follow',cl=cl,order=order))
    else:
        run = connect.Non_select("""DELETE FROM `follow` where `following`=%s and `follower`=%s"""%(id,g.user['ID']))
        flash('Unfollow successful','warning')
    return redirect(url_for('profile.profile',id = id))