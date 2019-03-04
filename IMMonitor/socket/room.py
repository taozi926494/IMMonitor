from flask import session
from flask_socketio import join_room
from IMMonitor.socket import socketio
from IMMonitor import ret_val


@socketio.on('join')
def on_join(data):
    '''
    加入一个用户自己的房间，实现多用户通信
    :param data: socket传过来的值
    :return: socket emit 加入房间状态
    '''
    params_username = data.get('username')
    session_username = session.get('user_id')
    if not params_username or session_username is None or params_username != session_username:
        retmsg = ret_val.gen(ret_val.CODE_SOCKET_ERR,
                             extra_msg='Can not join Room %s ！ 无法加入房间：%s'
                                             % (params_username, params_username))

        socketio.emit('check_join', data=retmsg)
        return

    join_room(session_username)
    retmsg = ret_val.gen(ret_val.CODE_SUCCESS,
                         extra_msg='Join room named %s successfully ! 成功加入房间'
                                         % (params_username, params_username))
    socketio.emit('check_join', data=retmsg, room=session_username)
    return
