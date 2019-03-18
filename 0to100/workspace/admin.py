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

    if request.method == 'POST'and request.form['action'] == "AD":
        f = request.files.get('file')
        base64_pic = image_to_base64(f)
        picture = bytes.decode(base64_pic)

        run = connect.Non_select("""INSERT INTO `AD` ( `picture`, \
            `title`, `caption`) VALUES ( '%s', '%s', '%s')"""%(picture,request.form['title'],request.form['caption']))
        flash('Upload successful','success')
        return redirect(url_for('admin.admin'))


    return render_template('admin/admin.html',AD=AD,len=len,range=range,report=report)

@bp.route('/del_AD/<int:id>',methods=('GET', 'POST'))
@login_required
@admin_required
def del_AD(id):
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `AD` WHERE `AD`.`ID` = %s"""%id)
    flash('Delete success','warning')
    return redirect(url_for('admin.admin'))
