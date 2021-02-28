# -*- coding: utf-8 -*-
# date: 2020/11/28 21:50

"""
频率限制
    - 发送短信
"""

from rest_framework.throttling import SimpleRateThrottle


class SMSThrottling(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        # key 唯一标识  cache_format = 'throttle_%(scope)s_%(ident)s'
        return self.cache_format % {'scope': self.scope, 'ident': mobile}

