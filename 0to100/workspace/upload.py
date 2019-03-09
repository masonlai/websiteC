import os

from workspace.database import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from workspace.database import *

from workspace.profile import image_to_base64

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/ok', methods=['GET', 'POST'])
def upload():
    app = current_app._get_current_object()
    if request.method == 'POST':
        connect = Database()
        connect.Connect_to_db()
        f = request.files.get('file')
        base64_pic = image_to_base64(f)
        picture = bytes.decode(base64_pic)

        run = connect.Non_select("""INSERT INTO `picture` (`ID`, `auth_ID`, \
        `picture`, `likes`,`collection`, `timestamp`) VALUES (NULL, '%s', '%s',\
         0, 0,CURRENT_TIMESTAMP);"""%(g.user['ID'],picture))

    return render_template('upload/upload.html')


