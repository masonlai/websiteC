import os

from flask import Flask
from flask_avatars import Avatars

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='CUproject',
    
    )

    avatars = Avatars(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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