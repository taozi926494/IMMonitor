from IMMonitor.db.common import db, Base
from flask_login import UserMixin
class User(UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def validLogin(cls, form):
        username = form.get('username')
        if username and User.query.filter_by(username=username).first():
            return True
