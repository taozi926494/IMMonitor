import json
from urllib.parse import urlencode
import requests
from aip import AipSpeech
import base64
# from IMMonitor.analysis import ACCESS_TOKEN, DETECT_URL_IMG, DETECT_URL_TEXT

APP_ID = '15674182'
API_KEY = 'X4gVrgxTl4KbqjAtOnMf0BCs'
SECRET_KEY = 'ofOfsvyKXlNpxEIADp2MkNbZitm6kDRL'
ACCESS_TOKEN = '24.ad351b35b33ecadfead85aec0b556ebf.2592000.1554274477.282335-15674182'
DETECT_URL_IMG = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/user_defined"
DETECT_URL_TEXT = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam'

def detect_image(image):
    """
    图像检测
    :param image: 二进制图像
    :param access_token: 百度AI平台access_token
    :return:
    成功返回：

    失败返回

    """
    # 待审核图片Base64编码字符串
    f = open(image, 'rb')
    image = base64.b64encode(f.read())
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
	
def recognize_speech(voice):
    """
    语音识别
    :param voice:语音文件的格式，pcm 或者 wav 或者 amr
    :param access_token: 百度AI平台access_token
    :return:
    --------------------------------------------------------------------------------------------
    参数	    |  类型	|是否一定输出	| 描述
    err_no	|  int	|    是	    | 错误码
    err_msg	|  int	|    是	    | 错误码描述
    sn	    |  int	|    是	    | 语音数据唯一标识，系统内部产生，用于 debug
    result	|  int	|    是	    | 识别结果数组，提供1-5 个候选结果，string 类型为识别的字符串， utf-8 编码
    --------------------------------------------------------------------------------------------
    成功返回：
    {
    "err_no": 0,
    "err_msg": "success.",
    "corpus_no": "15984125203285346378",
    "sn": "481D633F-73BA-726F-49EF-8659ACCC2F3D",
    "result": ["北京天气"]
    }
    失败返回：
    {
    "err_no": 2000,
    "err_msg": "data empty.",
    "sn": null
    }
    """
    data = 'ffmpeg -y  -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm'%(voice,voice)
    os.popen(data)
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 读取文件
    with open(voice + ".pcm", 'rb') as fp:
        # return fp.read()
        res_dict = client.asr(fp.read(),'pcm',16000, {'dev_pid': '1537'})
        if "result" not in res_dict:
            return res_dict
        else:
            result = res_dict["result"][0]
            return result