#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2018-12-12 09:40
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信联系人相关路由

from IMMonitor import app, ret_val
from IMMonitor.wx.contact import proxy
from flask import jsonify, Blueprint, session
from IMMonitor.wx.model import *
from IMMonitor import SESSION_KEY
from IMMonitor.wx.contact.utils import groups_name_from_contacts


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
        # 从联系人列表中提取出群列表
        group_name_list = groups_name_from_contacts(contact_list)
        print('group_name_list : ', group_name_list)
        # 存储群组的联系人信息
        group_contact_res = proxy.batch_get_group_contact(group_name_list)

        if group_contact_res['code'] == ret_val.CODE_SUCCESS:
            save_group_contact_list(group_contact_res['data']['group_contact_list'])
            return jsonify(ret_val.gen(ret_val.CODE_SUCCESS,
                                       data=group_contact_res['data']['group_contact_list'],
                                       extra_msg='提取群组信息成功'))
        else:
            return jsonify(group_contact_res)
    else:
        return jsonify(all_contact_res)


def save_group_contact_list(group_contact_list):
    """
    存储群组列表
    :param group_contact_list:
        [
            {
                'Uin': 0,
                'UserName': '@@9b94b78c20eb2ec5ee564d1a85af7d8353a125090a434ba59afdf95998e5ffdb',
                'NickName': '数据小群_ALL',
                'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=690212441
                            &username=@@9b94b78c20eb2ec5ee564d1a85af7d8353a125090a434ba59afdf95998e5ffdb&skey=',
                'ContactFlag': 3,
                'MemberCount': 8,
                'MemberList': [{
                      'Uin': 0,
                      'UserName': '@0cfdcbfa81ebc14c9300a048d50b41bd82169a02cbb37f46c1dc950ec577ecb2',
                      'NickName': '贵州大学黎万英',
                      'AttrStatus': 233573,
                      'PYInitial': '',
                      'PYQuanPin': '',
                      'RemarkPYInitial': '',
                      'RemarkPYQuanPin': '',
                      'MemberStatus': 0,
                      'DisplayName': '黎万英',
                      'KeyWord': ''
                    },
                    ...
                    ...
                ],
                'RemarkName': '',
                'HideInputBarFlag': 0,
            },
            ...
            ...
        ]
    :return:
    """
    user_uin = session[SESSION_KEY.WxLoginInfo]['uin']
    for group_contact in group_contact_list:
        group_member_list = group_contact.pop('MemberList')
        group_contact['user_uin'] = user_uin
        WxGroup.save(group_dict=group_contact)
        group_username = group_contact['UserName']
        group_nickname = group_contact['NickName']
        for group_member in group_member_list:
            group_member['user_uin'] = user_uin
            group_member['group_username'] = group_username
            group_member['group_nickname'] = group_nickname
            WxGroupMember.save(groupmember_dict=group_member)
