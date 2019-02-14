import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.datebase import Database

bp = Blueprint('login', __name__, url_prefix='/login')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login.login'))

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
		user = connect.select_func( 'SELECT user_name, password FROM user WHERE user_name = ?', (user_id,))
        .fetchone()
        g.user = user


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST'and request.form['first_name'] == None:
        username = request.form['username_login']
        password = request.form['password_login']
        error = None
        connect = Database()
        connect.Connect_to_db()
        user = connect.select_func( 'SELECT * FROM user WHERE user_name = ?', (username_login,))
        .fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)


    if request.method == 'POST' and request.form['username_login'] == None :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username_sigup']
        email = request.form['email']
        email_cf = request.form['email_confirm']
        password = request.form['password_signup']
        password_cf = request.form['password_confirm']
        connect = Database()
        connect.Connect_to_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username_sigup,)
        ).fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            run = connect.Non_select(
                'INSERT INTO user (username, password, first_name, last_name, gender, birthday) VALUES (?, ?)',
                (username, generate_password_hash(password), first_name, last_name, gender, birthday)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('login/login.html')