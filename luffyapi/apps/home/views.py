from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from luffyapi.utils.response import APIResponse

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from . import models
from . import serializer
from django.conf import settings

# class TestView(APIView):
#     def get(self, request, *args, **kwargs):
#         dic={'name': 'lqz'}
#         print(request.GET)
#         return APIResponse()

"""
写法一：
    路由：path('banner/', views.BannerView.as_view()),
"""


# class BannerView(GenericAPIView, ListModelMixin):
#     queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('display_order')
#     serializer_class = serializer.BannerModelSerializer


# 写法二
class BannerViewSet(GenericViewSet, ListModelMixin):
    # 设置最多展示3条
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNT]
    serializer_class = serializer.BannerModelSerializer
