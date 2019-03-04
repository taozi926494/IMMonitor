#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2018-12-11 18:01
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信相关基础函数

import logging

import requests
from IMMonitor import SESSION_KEY
from flask import session
from IMMonitor.wx.model import WxAccount

s = requests.session()

def getBaseRequest():
    """
    获取微信代理请求需要的 BaseRequest参数
    :return: dict 基础请求参数
    """
    loginInfo = session.get(SESSION_KEY.WxLoginInfo)

    # wx_account = WxAccount.query.filter_by(uin=session.get(SESSION_KEY.WxLoginInfo).get('uin')).first()
    # loginInfo = {}
    # loginInfo['skey'] = wx_account.skey
    # loginInfo['sid'] = wx_account.sid
    # loginInfo['uin'] = wx_account.uin
    # loginInfo['deviceid'] = wx_account.deviceid
    print('skey: %s, sid: %s, uin: %s, deviceid: %s' %
          (loginInfo.get('skey'), loginInfo.get('sid'), loginInfo.get('uin'), loginInfo.get('deviceid')))
    if not all(loginInfo.get(key) for key in ('skey', 'sid', 'uin', 'deviceid')):
        logging.error('BaseRequest is None because all skey,sid,uin,deviceid is not None')
        return None
    else:
        return {
            "Uin": loginInfo.get('uin'),
            "Sid": loginInfo.get('sid'),
            "Skey": loginInfo.get('skey'),
            "DeviceID": loginInfo.get('deviceid')
        }