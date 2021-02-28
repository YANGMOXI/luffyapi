# -*- coding: utf-8 -*-
# date: 2020/11/28 20:47

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from libs.tx_sms import settings
from luffyapi.utils.logger import log


def get_code():
    """生成一个4位数随机验证码"""
    import random
    s_code = ''
    for i in range(4):
        s_code += str(random.randint(0, 9))
    return s_code


def send_message(phone, code):
    """发送短信"""
    ssender = SmsSingleSender(settings.appid, settings.appkey)
    params = [code, "3"]  # 参数对应模板的{1}、{2}；无参数时，params = []
    try:
        result = ssender.send_with_param(86, phone, settings.template_id, params, sign=settings.sms_sign,
                                         extend="", ext="")
        print(result)
        if result.get('result') == 0:
            return True, result.get('errmsg')
        else:
            return False, result.get('errmsg')
    except Exception as e:
        log.error('手机号：%s短信发送失败, error: %s' % (phone, str(e)))


