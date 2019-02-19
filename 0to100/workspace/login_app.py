import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

bp = Blueprint('login_app', __name__, url_prefix='/login_app')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login_app.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        connect = Database()
        connect.Connect_to_db()
        user = connect.select_funcOne( 'SELECT * FROM user WHERE ID = '+str(user_id))
        g.user = user


@bp.route('/login', methods=('GET', 'POST'))
def login():
    connect = Database()
    connect.Connect_to_db()
    if request.method == 'POST'and request.form['action'] == "login":
        username = request.form['username_login']
        password = request.form['password_login']
        error = None
        user = connect.select_funcOne( """SELECT * FROM user WHERE username = '%s'""" %username)


        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(generate_password_hash(user['password']), password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['ID']
            return redirect(url_for('index'))

        flash(error)


    elif request.method == 'POST' and request.form['action'] == "register" :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username_signup']
        email = request.form['email']
        password = request.form['password_signup']
        password_cf = request.form['password_confirm']
        connect = Database()
        connect.Connect_to_db()
        error = None

        if connect.select_funcOne( """SELECT username FROM user WHERE username = '%s'""" %username) is not None:
            error = 'User {0} is already registered.'.format(username)
        elif password != password_cf:
            error = 'misspell for password'

        if error is None:
            run = connect.Non_select("""INSERT INTO `user` (`username`, `password`, 
            `first_name`, `last_name`, `email`) VALUES ('%s', '%s', '%s', '%s', '%s');"""
            %(username,password,first_name,last_name,email))


            run2 = connect.select_funcOne("""SELECT ID FROM user where username = '%s'""" %username)

            run3 = connect.Non_select("""INSERT INTO `Profile` (`ID`, `nick_name`, `gender`, `country`, `time_zone`, `status`) 
                VALUES ('%s', NULL, NULL, NULL, NULL, NULL);"""%run2['ID'])


            return redirect(url_for('login_app.login'))



        flash(error)

    return render_template('login_app/login.html')


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))