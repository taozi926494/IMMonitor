#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utils.py
# @Time    : 2018-12-12 09:23
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信联系人相关工具函数

from flask import session
from IMMonitor import SESSION_KEY
def groups_name_from_contacts(contact_list):
    """
    从联系人列表中返回群列表
    同时把群列表中的参数全部转化为小写
    :param contact_list:
    :return:
    """
    groups_name = []
    for contact in contact_list:
        user_name = contact['UserName']
        if '@@' in user_name:
            groups_name.append(user_name)
    return groups_name
