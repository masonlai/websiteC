import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

import datetime as dt

from workspace.login_app import login_required,admin_required

from workspace.profile import image_to_base64

bp = Blueprint('admin', __name__,url_prefix='/admin')

@bp.route('/', defaults={'page':'AD'} ,methods=('GET', 'POST'))
@bp.route('/<page>',methods=('GET', 'POST'))
@login_required
@admin_required
def admin(page):
    connect = Database()
    connect.Connect_to_db()
    AD = connect.select_funcALL("""SELECT * FROM `AD` ORDER BY`timestamp` DESC""")
    report = connect.select_funcALL("""SELECT * FROM `report` ORDER BY post_ID""")
    comment = connect.select_funcALL("""SELECT report_comment.comment_ID, comments.user_ID,\
        comments.pic_ID,comments.comments,COUNT(report_comment.comment_ID)FROM \
        report_comment,comments WHERE report_comment.comment_ID=comments.ID\
         and report_comment.status='exist' GROUP BY report_comment.comment_ID""")

    count_post_report = connect.select_funcALL("""SELECT picture.auth_ID,COUNT(*) FROM \
        `report`,picture WHERE picture.ID=report.post_ID GROUP BY picture.auth_ID""")

    count_comment_report = connect.select_funcALL("""SELECT comments.user_ID ,COUNT(*) FROM \
        report_comment,comments WHERE report_comment.comment_ID=comments.ID GROUP BY comments.user_ID""")
    ban_user=connect.select_funcALL("""SELECT ID FROM `user` WHERE `admin` = 'b'""")
    for i in range(len(count_post_report)):
        for a in range(len(count_comment_report)):
            if count_post_report[i]['auth_ID'] == count_comment_report[a]['user_ID']:
                count_post_report[i]['comment'] = count_comment_report[a]['COUNT(*)']
    for i in range(len(count_post_report)):
        try:
            count_post_report[i]['comment']
        except KeyError:
            count_post_report[i]['comment'] = 0
    i=0
    a=0
    c=0
    if len(ban_user) != 0:
        while i <len(count_post_report):
            if i == len(count_post_report)-c:
                if a < len(ban_user)-1:
                    a+=1
                    i=0

            if count_post_report[i]['auth_ID'] == ban_user[a]['ID']:
                ban_user[a]['comment'] = count_post_report[i]['comment']
                ban_user[a]['post']= count_post_report[i]['COUNT(*)']
                del(count_post_report[i])
                c+=1
                i-=1
            i+=1


    if request.method == 'POST'and request.form['action'] == "AD":
        f = request.files.get('file')
        base64_pic = image_to_base64(f)
        picture = bytes.decode(base64_pic)

        run = connect.Non_select("""INSERT INTO `AD` ( `picture`, \
            `title`, `caption`) VALUES ( '%s', '%s', '%s')"""%(picture,request.form['title'],request.form['caption']))
        flash('Upload successful','success')
        return redirect(url_for('admin.admin'))


    return render_template('admin/admin.html',AD=AD,len=len,range=range,ban_user=ban_user\
        ,report=report,comment=comment,str=str,count_post_report=count_post_report)

@bp.route('/del_AD/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def del_AD(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `AD` WHERE `AD`.`ID` = %s"""%id)
    flash('Delete success','warning')
    return redirect(url_for('admin.admin'))

@bp.route('/del_post/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def del_post(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `picture` WHERE `picture`.`ID` = %s"""%id)
    run2 = connect.Non_select("""DELETE FROM `report` WHERE `report`.`post_ID` = %s """%id)
    run3 = connect.Non_select("""DELETE FROM `comments` WHERE `comments`.`pic_ID` = %s """%id)
    flash('Delete success','warning')
    return redirect(url_for('admin.admin',_anchor='post'))

@bp.route('/del_comment/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def del_comment(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `comments` WHERE `comments`.`ID` = %s"""%id)
    run2 = connect.Non_select("""UPDATE `report_comment` SET `status` = \
        'ban' WHERE `report_comment`.`comment_ID` = %s """%id)
    flash('Delete success','warning')
    return redirect(url_for('admin.admin',_anchor='comment'))

@bp.route('/ban_user/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def ban_user(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""UPDATE `user` SET `admin` = 'b' WHERE `user`.`ID` = %s"""%id)
    flash('User was banned' ,'warning')
    return redirect(url_for('admin.admin',_anchor='ban'))

@bp.route('/unban_user/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def unban_user(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""UPDATE `user` SET `admin` = 'N' WHERE `user`.`ID` = %s"""%id)
    flash('User was unbanned' ,'success')
    return redirect(url_for('admin.admin',_anchor='unban'))