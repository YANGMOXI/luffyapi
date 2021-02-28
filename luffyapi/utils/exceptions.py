# -*- coding: utf-8 -*-
# date: 2020/11/11 16:57

"""
同一处理异常，并记录到日志
"""

from rest_framework.views import exception_handler as drf_exception_handler
from .response import APIResponse
from .logger import log


def common_exception_handler(exc, context):
    ret = drf_exception_handler(exc, context)
    if not ret:  # dr发内置处理不了，交给django-我们自己处理
        log.error('view: %s, 错误：%s' % (context['view'].__class__.__name__, str(exc)))  # 记录服务器异常
        # print(context['view'].__class__.__name__, str(exc))

        # 添加更细致的捕获异常
        if isinstance(exc, KeyError):
            return APIResponse(code=0, msg='key error')

        return APIResponse(code=0, msg='error', result=str(exc))  # code 成功：0；失败：0
    else:
        return APIResponse(code=0, msg='error', result=ret.data)