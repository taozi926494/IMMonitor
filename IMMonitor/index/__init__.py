from flask import render_template, Blueprint, session
from flask_login import login_required
from IMMonitor import app

bp_index = Blueprint('bp_index', __name__)

@app.route('/')
# @login_required
def index():
    return render_template('/index/index.html')