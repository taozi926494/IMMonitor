from flask_socketio import SocketIO, join_room
from flask import session
from IMMonitor import app


socketio = SocketIO(app)


from IMMonitor.socket.room import *