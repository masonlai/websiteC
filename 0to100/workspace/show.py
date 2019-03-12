from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

import datetime as dt



bp = Blueprint('show', __name__, url_prefix='/show')

@bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    connect = Database()
    connect.Connect_to_db()
    show_info = connect.select_funcOne("""SELECT * FROM `picture` WHERE `ID` = %s"""%id)
    auth_info = connect.select_funcOne("""SELECT Profile.nick_name, Profile.ID, Profile.icon FROM `picture` JOIN\
     Profile ON picture.auth_ID = Profile.ID where picture.auth_ID = '%s'"""%(show_info['auth_ID'],))
    comments = connect.select_funcALL("""SELECT \
        comments.comments, comments.timestamp, Profile.icon ,\
     Profile.nick_name ,Profile.ID FROM comments JOIN Profile ON comments.user_ID = Profile.ID WHERE comments.pic_ID = %s"""%id)

    for i in range(len(comments)):
        db = str(comments[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()

        if TD < 59:
            comments[i]['timestamp'] = str(int(TD))+'s ago'
        elif TD < 3599:
            comments[i]['timestamp'] = str(int(TD/60))+' mins ago'
        elif TD <215999:
            comments[i]['timestamp'] = str(int(TD/60/60))+' hours ago'
        elif TD <5183999:
            comments[i]['timestamp'] = str(int(TD/60/60/24))+' days ago'
        else:
            comments[i]['timestamp'] = str(int(TD/60/60/24/365))+' years ago'

    if request.method == 'POST' and request.form['submit'] == 'send':

        comments=request.form['comments']

        run = connect.Non_select("""INSERT INTO `comments` (`ID`, `pic_ID`,`user_ID`,`comments`, \
        `timestamp`) VALUES (NULL, '%s', '%s','%s',CURRENT_TIMESTAMP);"""%(id,g.user['ID'],comments))

        return redirect(url_for('show.show',id=id))

    if request.method == 'POST' and request.form['submit'] == 'edit':
        return redirect(url_for('upload.edit', id=show_info['ID']))

    return render_template('show/show.html',len=len,range=range, show_info=show_info, auth_info=auth_info,comments=comments)


