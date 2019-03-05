#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : proxy.py
# @Time    : 2018-12-12 15:54
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 微信登录相关请求代理

import base64
import io
import json
import random
import re
import time
from xml.dom import minidom

from flask import session
from pyqrcode import QRCode

from IMMonitor.wx import config, s, getBaseRequest
from IMMonitor.wx.utils import emoji_formatter
from IMMonitor import SESSION_KEY, ret_val


def _get_QRuuid():
    """
    从扫码登录接口获取uuid，拿到这个uuid之后才可以进行扫码登录
    :return: 扫码登录接口的uuid
    """

    '''
    -----------------------------------------------------------------------------------------------------
    | 接口地址 | https://login.weixin.qq.com/jslogin
    -----------------------------------------------------------------------------------------------------
    | 请求方法 | POST
    -----------------------------------------------------------------------------------------------------
    | 传递参数 |  appid:应用 ID，这个值是固定的
    |          |        网页版微信早期的值为 wx782c26e4c19acffb，在微信客户端上显示为应用名称为 Web 微信；
    |          |        现在用的是 wxeb7ec651dd0aefa9，显示名称为微信网页版
    |          |  fun: new 应用类型，这个值也是固定的
    -----------------------------------------------------------------------------------------------------
    |  返回值  |  {window.QRLogin.code = 200; window.QRLogin.uuid = "xxx"}
    -----------------------------------------------------------------------------------------------------
    '''
    session.permanent = True
    session[SESSION_KEY.WxLoginInfo] = {}

    # 组装请求url
    url = '%s/jslogin' % config.BASE_URL
    # 组装请求参数
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new', }
    # 组装请求头
    headers = {'User-Agent': config.USER_AGENT}
    # 请求扫码登录uuid
    for i in range(config.RETRY_TIMES):
        # 发起请求
        r = s.get(url, params=params, headers=headers)
        # 匹配返回值
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
        data = re.search(regx, r.text)
        # 提取uuid
        if data and data.group(1) == '200':
            # uuid = data.group(2)
            return data.group(2)


def get_QR():
    """
    根据扫码登录uuid生成登录二维码
    :param uuid: 扫码登录uuid
    :return: BytesIO 二维码二进制io流
    """
    uuid = _get_QRuuid()
    # 如果没有请求到扫码登录的uuid，返回错误
    if not uuid:
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Cannot get QRuuid ! 无法获取二维码扫码登录uuid !')

    else:
        session[SESSION_KEY.WxLoginInfo]['uuid'] = uuid
        qrStorage = io.BytesIO()
        qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
        qrCode.png(qrStorage, scale=10)
        return ret_val.gen(ret_val.CODE_SUCCESS, data={
                "qrcode": bytes.decode(base64.b64encode(qrStorage.getvalue()))
            })


def check_login():
    """
    检测用户是否已登录
    :param self:
    :param uuid: 扫描登录的uuid
    :return:    200 确认登录
                 201 扫描成功（还未按登录按钮）
                 204 现在正有一个检查登录请求在发送，不需要重复请求
                 408 一直未扫描（或者登陆超时）
                 400/424 代理出错
    """

    '''
    -----------------------------------------------------------------------------------------------------
    | 接口地址 | https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login
    -----------------------------------------------------------------------------------------------------
    | 请求方法 | GET
    -----------------------------------------------------------------------------------------------------
    |          | tip: 1 未扫描 0 已扫描 
    | 传递参数 | uuid: xxx 
    |          |  _: 时间戳
    -----------------------------------------------------------------------------------------------------
    |  返回值  |  window.code=xxx;
    |          |  xxx:
    |          |    200 确认登录
    |          |    201 扫描成功（还未按登录按钮）
    |          |    408 一直未扫描（或者登陆超时）
    |          |    400 424 代理出错
    |          |    
    |          | 当返回200时，在返回的body中，还会返回以下数据让前端重定向到登录后的页面，
    |          | window.redirect_uri="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=xxx&uuid=xxx&lang=xxx&scan=xxx";
    |          | 这里我们使用 proccess_login_info 函数再起发起该重定向地址的请求
    -----------------------------------------------------------------------------------------------------
    '''

    uuid = session.get(SESSION_KEY.WxLoginInfo).get('uuid')

    # 构造checklogin请求url及参数
    url = '%s/cgi-bin/mmwebwx-bin/login' % config.BASE_URL
    localTime = int(time.time())
    params = 'loginicon=true&uuid=%s&tip=1&r=%s&_=%s' % (
        uuid, int(-localTime / 1579), localTime)
    headers = {'User-Agent': config.USER_AGENT}

    # 发起请求
    r = s.get(url, params=params, headers=headers)
    regx = r'window.code=(\d+)'
    data = re.search(regx, r.text)

    # TODO: 扫码的时候返回用户头像用于显示
    # r.text = window.code=201;window.userAvatar = 'data:img/jpg;base64,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';

    # 如果是确认登录
    if not data:
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Regex extract nothing in check login response data ! 正则匹配没有在检测登录接口的返回值中匹配到任何信息 !')

    retcode = data.group(1)
    # 确认登录
    if retcode == '200':
        # 处理确认登录的返回结果
        print('login info: ', r.text)
        if process_login_info(r.text):
            # 登录之后设置checklogin为True
            return ret_val.gen(ret_val.CODE_SUCCESS)
        else:
            return ret_val.gen(ret_val.CODE_PROXY_ERR,
                               extra_msg='Error when process confirm login ! 处理确认登录时发送错误 !')
    else:
        return {
            "code": int(retcode),
            "status": "ok"
        }


def process_login_info(loginContent):
    """
    处理确认登录的返回结果
    当返回200时，在返回的body中，还会返回以下数据让前端重定向到登录后的页面，
    window.redirect_uri="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=xxx&uuid=xxx&lang=xxx&scan=xxx";
    """

    '''
     -----------------------------------------------------------------------------------------------------
    | 接口地址 | https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=xxx&uuid=xxx&lang=xxx&scan=xxx
    -----------------------------------------------------------------------------------------------------
    | 请求方法 | GET
    -----------------------------------------------------------------------------------------------------
    |          | ticket: 登录门票（确认登录后自动返回） 
    | 传递参数 | uuid: 微信uuid  （确认登录后自动返回） 
    |          | lang: zh_CN     （确认登录后自动返回） 
    |          | scan: xxx       （确认登录后自动返回） 
    -----------------------------------------------------------------------------------------------------
    |  返回值  |  xml格式
    |          | <error>
    |          |    <ret>0</ret>
    |          |    <message>OK</message>
    |          |    <skey>xxx</skey>
    |          |    <wxsid>xxx</wxsid>
    |          |    <wxuin>xxx</wxuin>
    |          |    <pass_ticket>xxx</pass_ticket>
    |          |    <isgrayscale>1</isgrayscale>
    |          | </error>
    -----------------------------------------------------------------------------------------------------
    '''
    # 处理返回结果
    regx = r'window.redirect_uri="(\S+)";'
    loginInfo = {}
    # 提取登录后重定向地址
    # 结果： https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=xxx&uuid=xxx&lang=xxx&scan=xxx
    loginInfo['url'] = re.search(regx, loginContent).group(1)
    headers = { 'User-Agent' : config.USER_AGENT }
    #发起重定向请求
    r = s.get(loginInfo['url'], headers=headers, allow_redirects=False)

    # 提取登录地址,放入登录信息中
    # 结果：https://wx.qq.com/cgi-bin/mmwebwx-bin
    loginInfo['url'] = loginInfo['url'][:loginInfo['url'].rfind('/')]

    # 微信可能有以下几个登录地址，根据我们得到的登录地址来确定文件上传 file 的地址以及同步刷新 webpush 地址
    for indexUrl, detailedUrl in (
            ("wx2.qq.com"      , ("file.wx2.qq.com", "webpush.wx2.qq.com")),
            ("wx8.qq.com"      , ("file.wx8.qq.com", "webpush.wx8.qq.com")),
            ("qq.com"          , ("file.wx.qq.com", "webpush.wx.qq.com")),
            ("web2.wechat.com" , ("file.web2.wechat.com", "webpush.web2.wechat.com")),
            ("wechat.com"      , ("file.web.wechat.com", "webpush.web.wechat.com"))):
        fileUrl, syncUrl = ['https://%s/cgi-bin/mmwebwx-bin' % url for url in detailedUrl]
        if indexUrl in loginInfo['url']:
            loginInfo['fileUrl'], loginInfo['syncUrl'] =  fileUrl, syncUrl
            break
        else:
            loginInfo['fileUrl'] = loginInfo['syncUrl'] = loginInfo['url']

    # 构造登录信息----设备Id
    # 值：e + 15位随机数
    loginInfo['deviceid'] = 'e' + repr(random.random())[2:17]
    # 构造登录信息----时间戳
    # 值：13位精确到毫秒
    loginInfo['logintime'] = int(time.time() * 1e3)
    loginInfo['BaseRequest'] = {}

    # 提取返回结果 xml格式
    for node in minidom.parseString(r.text).documentElement.childNodes:
        if node.nodeName == 'skey':
            loginInfo['skey'] = loginInfo['BaseRequest']['Skey'] = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            loginInfo['wxsid'] = loginInfo['BaseRequest']['Sid'] = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            loginInfo['wxuin'] = loginInfo['BaseRequest']['Uin'] = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            loginInfo['pass_ticket'] = loginInfo['BaseRequest']['DeviceID'] = node.childNodes[0].data

    if not all([key in loginInfo for key in ('skey', 'wxsid', 'wxuin', 'pass_ticket')]):
        return False

    session[SESSION_KEY.WxLoginInfo]['skey'] = loginInfo['skey']
    session[SESSION_KEY.WxLoginInfo]['sid'] = loginInfo['wxsid']
    session[SESSION_KEY.WxLoginInfo]['uin'] = loginInfo['wxuin']
    session[SESSION_KEY.WxLoginInfo]['passticket'] = loginInfo['pass_ticket']
    session[SESSION_KEY.WxLoginInfo]['logintime'] = loginInfo['logintime']
    session[SESSION_KEY.WxLoginInfo]['deviceid'] = loginInfo['deviceid']

    session[SESSION_KEY.WxLoginInfo]['url'] = loginInfo['url']
    session[SESSION_KEY.WxLoginInfo]['syncurl'] = loginInfo['syncUrl']
    session[SESSION_KEY.WxLoginInfo]['fileurl'] = loginInfo['fileUrl']

    return True


def web_init():
    """
    初始化微信首页栏的联系人、公众号等
    ** 最重要的是** 初始化登录者的信息（昵称、性别等），初始化同步消息所用的SycnKey
    :return: 用于信息列表
    """

    # 组装请求参数及url
    url = '%s/webwxinit' % session.get(SESSION_KEY.WxLoginInfo).get("url")
    params = {
        'r': int(-time.time() / 1579),
        'pass_ticket': session.get(SESSION_KEY.WxLoginInfo).get("passticket") }
    data = {'BaseRequest': getBaseRequest()}
    headers = {
        'ContentType': 'application/json; charset=UTF-8',
        'User-Agent': config.USER_AGENT, }

    # 发起请求获取返回结果
    r = s.post(url, params=params, data=json.dumps(data), headers=headers)
    dic = json.loads(r.content.decode('utf-8', 'replace'))

    if not dic or not dic.get('User').get('Uin'):
        return ret_val.gen(ret_val.CODE_PROXY_ERR,
                           extra_msg='Cannot get wx_init response ! 微信web_init接口未得到正确的返回结果')

    '''
    处理用户数据
    '''
    user_dict = {}
    emoji_formatter(dic['User'], 'NickName')  # 格式化昵称中的表情
    # 将返回的user信息与user_dict合并，userdict里面的键全小写
    for key in dic['User'].keys():
        user_dict[key.lower()] = dic['User'][key]

    user_dict['invitestartcount'] = int(dic['InviteStartCount'])
    user_dict['skey'] = dic['SKey']
    user_dict['synckeydict'] = dic['SyncKey']
    # 用于同步消息的 synckey  结果示例：1_690237487|2_690237829|3_690237697|1000_1545727682
    user_dict['synckey'] = '|'.join(['%s_%s' % (item['Key'], item['Val'])
        for item in dic['SyncKey']['List']])

    return ret_val.gen(ret_val.CODE_SUCCESS, data={
            "user_dict": user_dict
        })
