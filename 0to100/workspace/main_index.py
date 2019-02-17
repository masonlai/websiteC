import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *


bp = Blueprint('main_index', __name__,url_prefix='/main_index')

@bp.route('/main_page', methods=('GET', 'POST'))
def main_page():
    return render_template('main_index/main_page.html')