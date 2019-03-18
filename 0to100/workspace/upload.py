import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

from workspace.profile import image_to_base64

from workspace.login_app import login_required,unban_required

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/', methods=['GET', 'POST'])
@login_required
@unban_required
def upload():
    connect = Database()
    connect.Connect_to_db()
    
    if request.method == 'POST':
        try:
            f = request.files.get('file')
            caption =request.form['caption']
            title =request.form['title']


            check = connect.select_funcOne("""SELECT * FROM `picture` WHERE `title`='%s' """%title)

            if not check:

                base64_pic = image_to_base64(f)
                picture = bytes.decode(base64_pic)


                run = connect.Non_select("""INSERT INTO `picture` (`ID`, `auth_ID`,`title`,`caption`, \
                `picture`, `timestamp`) VALUES (NULL, '%s', '%s','%s','%s',\
                CURRENT_TIMESTAMP);"""%(g.user['ID'],title,caption,picture))

                show_info = connect.select_funcOne("""SELECT * FROM `picture` WHERE `auth_ID`='%s' and `title`='%s' and\
                `caption`='%s' and `picture`='%s'"""%(g.user['ID'],title,caption,picture))

                return redirect(url_for('show.show', id=show_info['ID']))
            else:
                flash('Title is repeated')
        except OSError as e:
            flash(e)

    edit='upload'
    return render_template('upload/upload.html',edit=edit)

@bp.route('/edit/<id>', methods=['GET', 'POST'])
@unban_required
@login_required
def edit(id):
    connect = Database()
    connect.Connect_to_db()
    show_info = connect.select_funcOne("""SELECT * FROM `picture` WHERE `ID` = %s"""%id)
    auth_info = connect.select_funcOne("""SELECT Profile.nick_name, Profile.ID FROM `picture` JOIN\
     Profile ON picture.auth_ID = Profile.ID where picture.auth_ID = '%s'"""%(show_info['auth_ID'],))
    if request.method == 'POST':
        title =request.form['title']
        caption =request.form['caption']
        run = connect.Non_select("""UPDATE `picture` SET `title`='%s',`caption`='%s' WHERE `ID` = '%s'"""%(title,caption,id))
        caption =request.form['caption']

        return redirect(url_for('show.show', id=show_info['ID']))
    edit='edit'
    return render_template('upload/upload.html',edit=edit,show_info=show_info, auth_info=auth_info)
