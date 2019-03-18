from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

import datetime as dt
from workspace.login_app import login_required


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
        comments = connect.select_funcALL("""SELECT comments.ID,\
                comments.comments, comments.timestamp, Profile.icon ,\
             Profile.nick_name ,Profile.ID FROM comments JOIN Profile \
             ON comments.user_ID = Profile.ID WHERE comments.pic_ID = %s  """%id)

        

    else:
        comments = connect.select_funcALL("""SELECT comments.ID,\
            comments.comments, comments.timestamp, Profile.icon ,\
         Profile.nick_name ,Profile.ID FROM comments JOIN Profile\
          ON comments.user_ID = Profile.ID WHERE comments.pic_ID = %s ORDER BY comments.timestamp DESC; """%id)

    if not not g.user:
        like = connect.select_funcOne("""select * from love where `love`.`love_ID` = %s AND `love`.`picture_ID` = %s"""%(g.user['ID'],id))
        report = connect.select_funcALL("""select * from report_comment where reporter_ID=%s"""%(g.user['ID']))
        for i in range(len(comments)):
            for a in range(len(report)):
                if comments[i]['ID'] == report[a]['comment_ID']:
                    comments[i]['reported'] = 'Y'
        follow = connect.select_funcOne("""select *from follow where following = %s and follower = %s"""%(show_info['auth_ID'],g.user['ID']))
        if not follow:
            check_follow='N'
        else:
            check_follow='Y'


        collection = connect.select_funcOne("""select * from collection WHERE `collection`.`picture_ID` = %s AND \
        `collection`.`collecter_ID` = %s"""%(id,g.user['ID']))

    else:
        like = None
        collection = None
        follow = None
        check_follow = 'N'

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
        elif TD <86399:
            comments[i]['timestamp'] = str(int(TD/60/60))+' hours ago'
        elif TD <31535999:
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
        try:
            if len(paginate[page-1]) == 10:
                page += 1
        except IndexError:
            pass
        return redirect(url_for('show.show',id=id,page=page,order=order))

    if request.method == 'POST' and request.form['submit'] == 'edit':
        return redirect(url_for('upload.edit', id=show_info['ID']))

    if request.method == 'POST' and request.form['submit'] == 'follow':
        return redirect(url_for('show.follow', id=show_info['auth_ID'],page=id,check_follow=check_follow))

    return render_template('show/show.html',len=len,range=range, show_info=show_info,\
        page=page, auth_info=auth_info,comments=comments,paginate=paginate,id=id,like=like,collection=collection,\
        likes=likes,collections=collections,order=order,str=str,check_follow=check_follow)


@bp.route('/<int:id>/like')
@login_required
def like(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""INSERT INTO `love` (`love_ID`, `picture_ID`) VALUES ('%s', '%s')"""%(g.user['ID'],id))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/collection')
@login_required
def collection(id):
    connect = Database()
    connect.Connect_to_db() 
    run = connect.Non_select("""INSERT INTO `collection` (`picture_ID`, `collecter_ID`) VALUES ('%s', '%s')"""%(id,g.user['ID']))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/unlike')
@login_required
def unlike(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `love` WHERE `love`.`love_ID` = %s AND `love`.`picture_ID` = %s"""%(g.user['ID'],id))
    return redirect(url_for('show.show',id=id))

@bp.route('/<int:id>/uncollect')
@login_required
def uncollection(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `collection` WHERE `collection`.`picture_ID` = %s AND \
        `collection`.`collecter_ID` = %s"""%(id,g.user['ID']))
    return redirect(url_for('show.show',id=id))


@bp.route('/report<int:id>', methods=['GET', 'POST'])
@login_required
def report(id):
    connect = Database()
    connect.Connect_to_db()
    post = connect.select_funcOne("""select picture.picture, picture.ID, picture.title, Profile.nick_name \
        from picture,Profile where picture.auth_ID = Profile.ID and picture.ID = %s"""%id)
    if not post:
        return redirect(url_for('main_index.main_page'))
    if request.method == 'POST':
        reson = request.form['reason']
        details = request.form['details']
        try:
            run = connect.Non_select("""INSERT INTO `report` (`post_ID`, `reporter_ID`, `reason`, `Details`) \
                VALUES ('%s', '%s', '%s', '%s')"""%(id,g.user['ID'],reson,details))
            flash('Reported','success')
        except pymysql.err.IntegrityError: 
            flash('You are already reported','danger')
        return redirect(url_for('show.show',id=id))

    return render_template('show/report.html',post=post)


@bp.route('/report_comment<int:id>/<int:comment>', methods=['GET', 'POST'])
@login_required
def report_comment(id,comment):
    connect = Database()
    connect.Connect_to_db()
    report = connect.select_funcOne("""select *from report_comment where comment_ID = %s and reporter_ID = %s"""%(comment,g.user['ID']))
    if not report:
        run = connect.Non_select("""INSERT INTO `report_comment` (`comment_ID`, `reporter_ID`) \
            VALUES ('%s', '%s')"""%(comment,g.user['ID']))
        flash('You reported the comment','warning')
    else:
        run = connect.Non_select("""DELETE FROM `report_comment` WHERE \
            `report_comment`.`comment_ID` = %s AND `report_comment`.`reporter_ID` = %s"""%(comment,g.user['ID']))
        flash('You cancel your report','success')


    return redirect(url_for('show.show',id=id))

@bp.route('/follow<int:id>/<int:page>/<check_follow>', methods=['GET', 'POST'])
@login_required
def follow(id,page,check_follow):
    connect = Database()
    connect.Connect_to_db()
    if check_follow == 'N':
        run = connect.Non_select("""INSERT INTO `follow` (`following`, `follower`,\
         `timestamp`) VALUES ('%s', '%s', CURRENT_TIMESTAMP)"""%(id,g.user['ID']))
        flash('Follow successful','success')
    else:
        run = connect.Non_select("""DELETE FROM `follow` where `following`=%s and `follower`=%s"""%(id,g.user['ID']))
        flash('Unfollow successful','warning')
    return redirect(url_for('show.show',id = page))