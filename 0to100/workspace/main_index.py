import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *


bp = Blueprint('main_index', __name__,url_prefix='/main_index')

@bp.route('/', defaults={'page':1},methods=('GET', 'POST'))
@bp.route('/<page>',methods=('GET', 'POST'))
def main_page(page):

    connect = Database()
    connect.Connect_to_db()

    main_pic = connect.select_funcALL("""SELECT `title`,`ID`,`picture`,`auth_ID` FROM `picture` ORDER BY`timestamp` LIMIT 9""")
    row=[]

    for i in range(0,len(main_pic),3):
        row.append(main_pic[i:i+3])



    return render_template('main_index/main_page.html',row=row,page=page,len=len)


