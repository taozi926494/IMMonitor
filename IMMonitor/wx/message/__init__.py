#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2018-12-12 10:05
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信消息相关路由

from IMMonitor import app, ret_val
from IMMonitor.wx.message import proxy, utils
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
    # 从代理拉取新消息
    ret = proxy.get_msg()
    if ret['code'] == ret_val.CODE_SUCCESS:
        # 消息列表
        AddMsgList = ret['data']['AddMsgList']
        group_msg_list = []
        if AddMsgList:
            group_msg_list = utils.produce_group_msg(AddMsgList)
        return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                   data=group_msg_list))
        # 联系人变动列表
        # TODO 处理联系人变动
        ModContactList = ret['data']['ModContactList']

    else:
        return jsonify(ret)
