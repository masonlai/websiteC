from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

import datetime as dt



bp = Blueprint('show', __name__, url_prefix='/show')

@bp.route('/<int:id>',defaults={'page':1,'order':1}, methods=['GET', 'POST'])
@bp.route('/<int:id><int:page><int:order>', methods=['GET', 'POST'])
def show(id,page,order):
    connect = Database()
    connect.Connect_to_db()

    show_info = connect.select_funcOne("""SELECT * FROM `picture` WHERE `ID` = %s"""%id)

    auth_info = connect.select_funcOne("""SELECT Profile.nick_name, Profile.ID, Profile.icon FROM `picture` JOIN\
     Profile ON picture.auth_ID = Profile.ID where picture.auth_ID = '%s' """%(show_info['auth_ID'],))

    if order == 2:
        comments = connect.select_funcALL("""SELECT \
                comments.comments, comments.timestamp, Profile.icon ,\
             Profile.nick_name ,Profile.ID FROM comments JOIN Profile \
             ON comments.user_ID = Profile.ID WHERE comments.pic_ID = %s  """%id)
    else:
        comments = connect.select_funcALL("""SELECT \
            comments.comments, comments.timestamp, Profile.icon ,\
         Profile.nick_name ,Profile.ID FROM comments JOIN Profile\
          ON comments.user_ID = Profile.ID WHERE comments.pic_ID = %s ORDER BY comments.timestamp DESC; """%id)



    if not not g.user:
        like = connect.select_funcOne("""select * from love where `love`.`love_ID` = %s AND `love`.`picture_ID` = %s"""%(g.user['ID'],id))

        collection = connect.select_funcOne("""select * from collection WHERE `collection`.`picture_ID` = %s AND \
        `collection`.`collecter_ID` = %s"""%(id,g.user['ID']))

    likes = connect.select_funcALL("""select * from love where `love`.`picture_ID` = %s"""%id)
    collections = connect.select_funcALL("""select * from collection WHERE `collection`.`picture_ID` = %s"""%id)

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

    paginate = []
    for i in range(0,len(comments),10):
        paginate.append(comments[i:i+10])

    if len(paginate)< (page-1):
        page = 1

    if request.method == 'POST' and request.form['submit'] == 'send':

        comments=request.form['comments']

        run = connect.Non_select("""INSERT INTO `comments` (`ID`, `pic_ID`,`user_ID`,`comments`, \
        `timestamp`) VALUES (NULL, '%s', '%s','%s',CURRENT_TIMESTAMP);"""%(id,g.user['ID'],comments))

        if len(paginate[page-1]) == 10:
            page += 1
        return redirect(url_for('show.show',id=id,page=page,order=order))

    if request.method == 'POST' and request.form['submit'] == 'edit':
        return redirect(url_for('upload.edit', id=show_info['ID']))

    return render_template('show/show.html',len=len,range=range, show_info=show_info,\
        page=page, auth_info=auth_info,comments=comments,paginate=paginate,id=id,like=like,collection=collection,\
        likes=likes,collections=collections,order=order)


@bp.route('/<int:id>/like')
def like(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""INSERT INTO `love` (`love_ID`, `picture_ID`) VALUES ('%s', '%s')"""%(g.user['ID'],id))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/collection')
def collection(id):
    connect = Database()
    connect.Connect_to_db() 
    run = connect.Non_select("""INSERT INTO `collection` (`picture_ID`, `collecter_ID`) VALUES ('%s', '%s')"""%(id,g.user['ID']))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/unlike')
def unlike(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `love` WHERE `love`.`love_ID` = %s AND `love`.`picture_ID` = %s"""%(g.user['ID'],id))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/uncollect')
def uncollection(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `collection` WHERE `collection`.`picture_ID` = %s AND \
        `collection`.`collecter_ID` = %s"""%(id,g.user['ID']))
    return redirect(url_for('show.show',id=id))