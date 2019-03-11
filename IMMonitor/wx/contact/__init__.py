#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2018-12-12 09:40
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信联系人相关路由
import hashlib
import os

from IMMonitor import app, ret_val
from IMMonitor.wx.contact import proxy
from flask import jsonify, Blueprint, request
from IMMonitor.wx.contact.utils import groups_username_from_contacts, save_group_contact_list

bp_wx_contact = Blueprint('bp_wx_contact', __name__)


@app.route('/wx/contact/get_contact')
def get_contact():
    all_contact = proxy.get_contact()
    return jsonify(all_contact)


@app.route('/wx/contact/get_group_contact')
def get_group_contact():
    """
    获取群组数据
    :return:
    """
    # 获取所有联系人的列表
    all_contact_res = proxy.get_contact()
    if all_contact_res['code'] == 200:
        contact_list = all_contact_res['data']['contact_list']
        # contact_list  [{'Uin': 0, 'UserName': '@885aa7efdd2a35804fb0459a5b1b67f2', 'NickName': '该帐号已冻结' ......
        # if contact_list[0]['Uin'] == 0:
        #     return jsonify(ret_val.gen(ret_val.CODE_PROXY_ERR, extra_msg=contact_list[0]['NickName']))

        # 从联系人列表中提取出群列表
        group_name_list = groups_username_from_contacts(contact_list)
        # 存储群组的联系人信息
        group_contact_res = proxy.batch_get_group_contact(group_name_list)

        if group_contact_res['code'] == ret_val.CODE_SUCCESS:
            group_contact_list = group_contact_res['data']['group_contact_list']

            # 对群做筛选
            utils.filter_group_contact_list(group_contact_list)

            save_group_contact_list(group_contact_list)

            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data=group_contact_list,
                                       extra_msg='提取群组信息成功'))
        else:
            return jsonify(group_contact_res)
    else:
        return jsonify(all_contact_res)


@app.route('/wx/contact/get_member_head_img')
def get_member_head_img():
    # 群组信息
    group_id = request.args.get('group_id')
    encry_chatroom_id = request.args.get('encry_chatroom_id')
    # 成员信息
    username = request.args.get('username')
    user_nickname = request.args.get('user_nickname')
    # TODO: 强制要求头像更新
    force = request.args.get('user_nickname')

    if not all((group_id, encry_chatroom_id, username, user_nickname)):
        return jsonify(ret_val.gen(ret_val.CODE_PARAMS_ERR,
                                   extra_msg='需要传入 group_id, encry_chatroom_id, username, user_nickname'))

    filedir = 'IMMonitor/static/wxheadimg/'
    filename = '%s%s' % (group_id, user_nickname)
    filename = hashlib.md5(filename.encode('utf8')).hexdigest()
    file_format = '.png'
    file = '{filedir}{filename}{file_format}'.format(filedir=filedir,
                                                     filename=filename,
                                                     file_format=file_format)
    # 不存在头像才请求新的
    if not os.path.exists(file):
        bit_img = proxy.get_member_head_img(EncryChatRoomId=encry_chatroom_id, username=username)
        if len(bit_img) > 10:
            with open(file, 'wb') as f:
                f.write(bit_img)

            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data={'FilePath': file.replace('IMMonitor', '')}))
        else:
            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data={'FilePath': '/static/wxheadimg/default.png'}))

    # 存在头像了返回原来的头像
    else:
        return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                   data={'FilePath': file.replace('IMMonitor', '')}))

@app.route('/wx/contact/get_head_img')
def get_head_img():
    username = request.args.get('username')
    group_id = request.args.get('group_id')
    uin = request.args.get('uin')
    if not username:
        return jsonify(ret_val.gen(ret_val.CODE_PARAMS_ERR,
                                   extra_msg='需要传入username'))

    filedir = 'IMMonitor/static/wxheadimg/'
    file_format = '.png'

    if uin:
        file = '{filedir}user_{filename}{file_format}'.format(filedir=filedir,
                                                         filename=uin,
                                                         file_format=file_format)
        # 不存在头像才请求新的
        if not os.path.exists(file):
            bit_img = proxy.get_head_img(username=username, type=0)
            if len(bit_img) > 10:
                with open(file, 'wb') as f:
                    f.write(bit_img)

                return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                           data={'FilePath': file.replace('IMMonitor', '')}))
            else:
                return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                           data={'FilePath': '/static/wxheadimg/default.png'}))

        # 存在头像了返回原来的头像
        else:
            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data={'FilePath': file.replace('IMMonitor', '')}))
    elif group_id:
        file = '{filedir}group_{filename}{file_format}'.format(filedir=filedir,
                                                         filename=group_id,
                                                         file_format=file_format)
        # 不存在头像才请求新的
        if not os.path.exists(file):
            bit_img = proxy.get_head_img(username=username, type=1)
            if len(bit_img) > 10:
                with open(file, 'wb') as f:
                    f.write(bit_img)

                return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                           data={'FilePath': file.replace('IMMonitor', '')}))
            else:
                return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                           data={'FilePath': '/static/wxheadimg/default.png'}))

        # 存在头像了返回原来的头像
        else:
            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data={'FilePath': file.replace('IMMonitor', '')}))
