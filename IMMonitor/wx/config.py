#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2018-12-12 14:07
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 基础配置

RETRY_TIMES = 5
TIMEOUT = (10, 60)
BASE_URL = 'https://login.weixin.qq.com'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

# 消息类型
MSG_TEXT = 'Text'  # 文字
MSG_MAP = 'Map'  # 地图
MSG_IMAGE = 'Image'  # 图片
MSG_AUDIO = 'Audio'  # 音频
MSG_VIDEO = 'Video'  # 视频
# NAME_CARD = 'NameCard'  # 名片
# FRIEND = 'Friend'  # 朋友
# CHAT_HISTORY = 'ChatHistory'  # 聊天记录
# SHARING_MEDIA = 'Sharing'  # 分享链接