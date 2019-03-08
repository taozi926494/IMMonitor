#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : proxy.py
# @Time    : 2018-12-12 09:11
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信联系人请求代理

import json
import logging
import time

from flask import session

from IMMonitor.wx import config, s, getBaseRequest
from IMMonitor import SESSION_KEY, db
from IMMonitor import ret_val

def get_contact():
    """
    获取联系人信息代理
    包括：普通联系人、群组、公众号
    :return: list 联系人列表
    """
    url = '%s/webwxgetcontact?r=%s&seq=%s&skey=%s' % (session[SESSION_KEY.WxLoginInfo].get('url'), int(time.time()),
                                                      0, session[SESSION_KEY.WxLoginInfo].get('skey'))

    # url = '%s/webwxgetcontact?r=%s&seq=%s&skey=%s' % (session[SESSION_KEY.WxLoginInfo].get('url'), 1543823795,
    #                                                   0, session[SESSION_KEY.WxLoginInfo].get('skey'))
    headers = {
        'ContentType': 'application/json; charset=UTF-8',
        'User-Agent': config.USER_AGENT}

    try:
        r = s.get(url, headers=headers)
    except:
        logging.error('Failed to fetch contact, that may because of the amount of your chatrooms')
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Error when requesting get_contact ! 请求get_contact接口出错 !')

    contact = json.loads(r.content.decode('utf-8', 'replace'))
    if contact['BaseResponse']['Ret'] == 0:
        return ret_val.gen(ret_val.CODE_SUCCESS, data={
                "contact_list": contact.get('MemberList')
            })
    else:
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Failed to fetch contact ! 无法正确获得联系人返回结果 !')


def batch_get_group_contact(group_name_list):
    """
    批量获取群组详细信息
    :param group_name_list: 群组列表
    :return: 群组详细信息列表
    """
    url = '%s/webwxbatchgetcontact?type=ex&r=%s' % (
        session[SESSION_KEY.WxLoginInfo]['url'], int(time.time()))

    headers = {
        'ContentType': 'application/json; charset=UTF-8',
        'User-Agent': config.USER_AGENT}

    data = {
        'BaseRequest': getBaseRequest(),
        'Count': len(group_name_list),
        'List': [{'UserName': GroupUserName, 'ChatRoomId': ''} for GroupUserName in group_name_list]
    }

    contact = json.loads(s.post(url, data=json.dumps(data), headers=headers
                                     ).content.decode('utf8', 'replace'))

    if contact['BaseResponse']['Ret'] == 0:
        return ret_val.gen(ret_val.CODE_SUCCESS, data={
                "group_contact_list": contact.get('ContactList')
            })
    else:
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Failed to fetch contact ! 无法正确获得联系人返回结果 !')

