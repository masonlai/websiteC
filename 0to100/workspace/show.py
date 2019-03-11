from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *




bp = Blueprint('show', __name__, url_prefix='/show')

@bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    connect = Database()
    connect.Connect_to_db()
    show_info = connect.select_funcOne("""SELECT * FROM `picture` WHERE `ID` = %s"""%id)
    auth_info = connect.select_funcOne("""SELECT Profile.nick_name, Profile.ID FROM `picture` JOIN\
     Profile ON picture.auth_ID = Profile.ID where picture.auth_ID = '%s'"""%(show_info['auth_ID'],))
    if request.method == 'POST':
    	return redirect(url_for('upload.edit', id=show_info['ID']))

    return render_template('show/show.html', show_info=show_info, auth_info=auth_info)

