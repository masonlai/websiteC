

from workspace.database import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)


bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/ok', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')  # 获取图片文件对象
        filename = random_filename(f.filename)  # 生成随机文件名
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
                 # 保存图片文件

    return render_template('upload/upload.html')