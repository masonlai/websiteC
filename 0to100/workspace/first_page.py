
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('login', __name__)

@bp.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST' and request.form['action'] == "search":
        search = request.form['Search']
        return redirect(url_for('main_index.search_page',search=search))
    return render_template('index.html')