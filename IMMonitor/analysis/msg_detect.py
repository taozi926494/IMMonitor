import json
from urllib.parse import urlencode
import requests

from IMMonitor.analysis import ACCESS_TOKEN, DETECT_URL_IMG, DETECT_URL_TEXT


def detect_image(image):
    """
    图像检测
    :param image: 二进制图像
    :param access_token: 百度AI平台access_token
    :return:
    成功返回：

    失败返回

    """

    # 二进制方式打开图片文件
    params = {"image": image}
    params = urlencode(params)

    # 百度人工智能API请求
    request_url = DETECT_URL_IMG + "?access_token=" + ACCESS_TOKEN
    res = requests.post(request_url, data=params)
    res_data = res.content.decode('utf-8')
    res_dict = json.JSONDecoder().decode(res_data)
    return res_dict


def detect_text(text, access_token):
    """
    文字检测
    :param text: 检测文字
    :param access_token: 百度AI平台access_token
    :return:
    """
    params = {"content": text}
    params = urlencode(params)
    # 百度人工智能API请求示例
    request_url = DETECT_URL_TEXT + "?access_token=" + ACCESS_TOKEN
    res = requests.post(request_url, data=params)
    res_data = res.content.decode('utf-8')
    res_dict = json.JSONDecoder().decode(res_data)
    return res_dict.get('result')

