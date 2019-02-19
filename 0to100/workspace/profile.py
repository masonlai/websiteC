import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *


bp = Blueprint('profile', __name__,url_prefix='/profile')

@bp.route('/profile_edit', methods=('GET', 'POST'))
def main_page():
    connect = Database()
    connect.Connect_to_db()
    if request.method == 'POST':
    	nick_name = request.form['Nick_name']
    	gender = request.form['Gender']
    	country = request.form['Country']
    	company =request.form['Company']
    	time_zone = request.form['Time_zone']
    	status = request.form['Status']
    return render_template('profile/profile_edit.html')