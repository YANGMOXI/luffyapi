# -*- coding: utf-8 -*-
# date: 2020/11/11 22:13

from django.urls import path, re_path, include
from . import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(prefix='banner', viewset=views.BannerViewSet, basename='banner')


urlpatterns = [
    path('', include(router.urls))
]