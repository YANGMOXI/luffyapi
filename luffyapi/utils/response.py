# -*- coding: utf-8 -*-
# date: 2020/11/11 16:36

from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=100, msg='成功', result=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if result:
            dic['result'] = result
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=None, content_type=content_type)


"""
dic.update:
    如果被更新的字典中己包含对应的键值对，那么原 value 会被覆盖；
    如果被更新的字典中不包含对应的键值对，则该键值对被添加进去。
        a = {'one': 1, 'two': 2, 'three': 3}
        a.update({'one':4.5, 'four': 9.3})
        print(a)
        运行结果为：
        {'one': 4.5, 'two': 2, 'three': 3, 'four': 9.3}
"""
