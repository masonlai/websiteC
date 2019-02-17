
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('login', __name__)

@bp.route('/')
def index():
    return render_template('index.html')