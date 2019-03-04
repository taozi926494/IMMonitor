#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : common.py
# @Time    : 2019-3-3 21:20
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 数据库的公有基础信息

import datetime
import os

from IMMonitor import app
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'IMMonitor.db')
db = SQLAlchemy(app, session_options=dict(autocommit=False, autoflush=True))


@app.teardown_request
def teardown_request(exception):
    """
    每一个请求之后该函数，遇到了异常使数据库回滚
    :param exception:
    :return:
    """
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


def get_china_time():
    """
    获取中国制时区时间
    :return: datetime
    """
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))


class Base(db.Model):
    """
    数据库的基类，包含自增id，创建时间，自动更新的修改时间
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=get_china_time)
    date_modified = db.Column(db.DateTime, default=get_china_time, onupdate=get_china_time)