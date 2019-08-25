import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

from flask_mail import Mail, Message

from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from threading import Thread



mail = Mail()

bp = Blueprint('login_app', __name__, url_prefix='/login_app')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login_app.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['admin'] == 'N':
            return redirect(url_for('main_index.main_page'))

        return view(**kwargs)

    return wrapped_view


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            flash('You should logout','danger')
            return redirect(url_for('main_index.main_page'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        connect = Database()
        connect.Connect_to_db()
        sql = 'SELECT * FROM user WHERE ID = %s'
        user = connect.select_funcOne( sql,str(user_id))
        g.user = user
        try:
            sql = """SELECT * FROM `Profile` WHERE `ID` = %s"""
            profile_info = connect.select_funcOne(sql,g.user['ID'])
        except:
            session.clear()
            return redirect(url_for('index'))
        g.profile_info = profile_info


@bp.route('/login', methods=('GET', 'POST'))
@logout_required
def login():
    if request.method == 'POST' and request.form['action'] == "search":
        search = request.form['Search']
        return redirect(url_for('main_index.search_page',search=search))
    connect = Database()
    connect.Connect_to_db()
    if request.method == 'POST'and request.form['action'] == "login":
        username = request.form['username_login']
        password = request.form['password_login']
        error = None
        sql =  """SELECT * FROM user WHERE username = %s""" 
        user = connect.select_funcOne(sql, username)


        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(generate_password_hash(user['password']), password):
            error = 'Incorrect password.'
        elif user['vaildation'] == 'N':
            session['vaildate'] = username
            return redirect(url_for('login_app.resend'))


        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['ID']
            return redirect(url_for('main_index.main_page'))

        flash(error,'danger')


    elif request.method == 'POST' and request.form['action'] == "search" :
        search =request.form['search']

        pass



    elif request.method == 'POST' and request.form['action'] == "register" :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username_signup']
        email = request.form['email']
        password = request.form['password_signup']
        password_cf = request.form['password_confirm']
        error = None

        sql = """SELECT username FROM user WHERE username = %s"""

        result = connect.select_funcOne(sql,username)

        if result is not None:
            error = 'User {0} is already registered.'.format(username)
        elif password != password_cf:
            error = 'misspell for password'

        if error is None:
            sql = """INSERT INTO `user` (`username`, `password`,
            `first_name`, `last_name`, `email`, `vaildation`) VALUES (%s, %s, %s, %s, %s, %s);"""
            run = connect.Non_select(sql,username,password,first_name,last_name,email,'N')
            a = 'No_show'
            sql = """SELECT ID, username FROM user where username = %s"""
            run2 = connect.select_funcOne(sql, username)
            sql = """INSERT INTO `Profile` (`ID`, `nick_name`, `gender`, `country`, `company`,`time_zone`, `status`, `background`, `icon`)
                VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s);"""
            run3 = connect.Non_select(sql,run2['ID'],run2['username'],a,a,a,a,a,'#5083b6','default')


            error = 'please go to your email and verify your email address'


            session.clear()

            session['vaildate'] = username

            sql =  """SELECT * FROM user WHERE username = %s""" 
            user = connect.select_funcOne(sql,session['vaildate'])
            subject = "Nonamela vaildation"
            to = user['email']
            token = generate_token(session['vaildate'],'vaildate')

            body =  render_template('login_app/confirm.txt', username=session['vaildate'], token=token)
            app = current_app._get_current_object()
            mail.init_app(app)
            send_smtp_mail(subject, to, body)


        flash(error,'danger')

    return render_template('login_app/login.html')


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))

def send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_smtp_mail(subject, to, body):
    app = current_app._get_current_object()  # if use factory (i.e. create_app()), get app like this
    message = Message(subject, recipients=[to], body=body)
    thr = Thread(target=send_async_mail, args=[app, message])
    thr.start()
    return thr


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def generate_token(user, operation, expire_in=None):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user, 'operation': operation}

    return s.dumps(data)


@bp.route('/confirm/<token>')
def confirm(token):

    flash('Account confirmed.','success')

    connect = Database()
    connect.Connect_to_db()
    sql = """UPDATE `user` SET `vaildation` = '%s' WHERE `username` = %s"""
    run = connect.Non_select(sql,'Y',session['vaildate'])

    return redirect(url_for('login_app.login'))



def validate_token(user, token, operation):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user != data.get('id'):
        return False

    return True


@bp.route('/vaildation/resend',methods=('GET', 'POST'))
def resend():
    resend = 0
    if request.method == 'POST':
        connect = Database()
        connect.Connect_to_db()
        sql = """SELECT * FROM user WHERE username = %s"""
        user = connect.select_funcOne( sql, session['vaildate'])
        subject = "Nonamela vaildation"
        to = user['email']
        token = generate_token(session['vaildate'],'vaildate')

        body =  render_template('login_app/confirm.txt', username=session['vaildate'], token=token)
        app = current_app._get_current_object()
        mail.init_app(app)
        send_smtp_mail(subject, to, body)
        resend =+ 1


    return render_template('login_app/resend.html',resend=resend)