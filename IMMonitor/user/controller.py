from IMMonitor import app, login_manager
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, request, session, redirect, render_template, url_for
from IMMonitor.user.model import *

ctrl_user_bp = Blueprint('ctrl_spider', __name__)

@login_manager.user_loader
def load_user(username):
    user = User.query.filter_by(username=username).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('User.validLogin(request.form)', User.validLogin(request.form))
        if User.validLogin(request.form):
            logined = login_user(load_user(username=request.form.get('username')))
            print('is logined?', logined)
            next = request.args.get('next')
            print(session)
            print(next, url_for('index'))
            return redirect(next or url_for('index'))
        else:
            return redirect('/login')

    if request.method == 'GET':
        return render_template('/user/login.html')


