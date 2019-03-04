#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2018-12-12 10:05
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信消息相关路由

from IMMonitor import app
from IMMonitor.wx.message import proxy
from flask import jsonify, Blueprint, session
from IMMonitor.wx.model import WxAccount
from IMMonitor import SESSION_KEY


bp_wx_message = Blueprint('bp_wx_message', __name__)
@app.route('/wx/message/sync_check')
def sync_chech():
    ret = proxy.sync_check()
    return jsonify(ret)

@app.route('/wx/message/get_msg')
def get_msg():
    ret = proxy.get_msg()
    return jsonify(ret)