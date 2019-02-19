import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'workspace.sql'),
    )

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



    app.add_url_rule('/', endpoint='index')

    return app