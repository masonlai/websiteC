import os

from flask import Flask
from flask_avatars import Avatars
from flask_mail import Mail, Message
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='CUproject',
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='nonamelascope@gmail.com',
        MAIL_PASSWORD='vai12121',
        MAIL_DEFAULT_SENDER=('Mason Lai', 'vai12121')
    )

    avatars = Avatars(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from workspace import database

    from workspace import first_page
    app.register_blueprint(first_page.bp)

    from workspace import login_app, main_index, profile
    app.register_blueprint(login_app.bp)
    app.register_blueprint(main_index.bp)
    app.register_blueprint(profile.bp)
    basedir = os.path.abspath(os.path.dirname(__name__))
    app.config['AVATARS_SAVE_PATH'] = os.path.join(basedir, 'avatars')
    app.add_url_rule('/', endpoint='index')

    return app