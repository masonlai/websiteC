import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

from workspace.profile import image_to_base64

from workspace.login_app import login_required

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and request.form['action'] == "search":
        search = request.form['Search']
        return redirect(url_for('main_index.search_page',search=search))
    connect = Database()
    connect.Connect_to_db()
    
    if request.method == 'POST':
        try:
            f = request.files.get('file')
            caption =request.form['caption']
            title =request.form['title']

            sql = """SELECT * FROM `picture` WHERE `title`= %s  """
            check = connect.select_funcOne(sql, title)

            if not check:

                base64_pic = image_to_base64(f)
                picture = bytes.decode(base64_pic)

                sql = """INSERT INTO `picture` (`ID`, `auth_ID`,`title`,`caption`, \
                `picture`, `timestamp`) VALUES (NULL,  %s ,  %s , %s , %s ,\
                CURRENT_TIMESTAMP);"""
                run = connect.Non_select(sql, g.user['ID'],title,caption,picture)

                sql = """SELECT * FROM `picture` WHERE `auth_ID`= %s  and `title`= %s  and\
                `caption`= %s  and `picture`= %s """
                show_info = connect.select_funcOne(sql, g.user['ID'],title,caption,picture)

                return redirect(url_for('show.show', id=show_info['ID']))
            else:
                flash('Title is repeated')
        except OSError as e:
            flash(e)

    edit='upload'
    return render_template('upload/upload.html',edit=edit)

@bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST' and request.form['action'] == "search":
        search = request.form['Search']
        return redirect(url_for('main_index.search_page',search=search))
    connect = Database()
    connect.Connect_to_db()
    sql = """SELECT * FROM `picture` WHERE `ID` = %s"""
    show_info = connect.select_funcOne(sql, id)
    sql = """SELECT Profile.nick_name, Profile.ID FROM `picture` JOIN\
     Profile ON picture.auth_ID = Profile.ID where picture.auth_ID = %s"""
    auth_info = connect.select_funcOne(sql, show_info['auth_ID'],)
    if request.method == 'POST':
        title =request.form['title']
        caption =request.form['caption']
        sql = """UPDATE `picture` SET `title`= %s ,`caption`= %s  WHERE `ID` =  %s """
        run = connect.Non_select(sql, title,caption,id)
        caption =request.form['caption']

        return redirect(url_for('show.show', id=show_info['ID']))
    edit='edit'
    return render_template('upload/upload.html',edit=edit,show_info=show_info, auth_info=auth_info)
