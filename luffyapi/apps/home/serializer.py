# -*- coding: utf-8 -*-
# date: 2020/11/14 22:15

from rest_framework import serializers
from . import models


class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ['name', 'img', 'link']
