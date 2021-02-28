# -*- coding: utf-8 -*-
# date: 2020/11/14 21:45
from django.db import models

"""
基类-抽象表
"""


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    orders = models.IntegerField()

    class Meta:
        abstract = True
