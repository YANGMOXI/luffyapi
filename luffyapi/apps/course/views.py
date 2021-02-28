from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from . import models
from . import serializer


class CourseCategoryView(GenericViewSet, ListModelMixin):
    """课程分类群查"""
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = serializer.CourseCategorySerializer


from .paginations import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
class CourseView(GenericViewSet, ListModelMixin):
    """课程群查"""
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination # 分页器

    # 过滤和排序
    filter_backends = [OrderingFilter]
    ordering_fields = ['id','price', 'students']
    # search 不支持关联字段，django-filter在其基础上增加了

from django_filters.rest_framework import DjangoFilterBackend
# 一个课程的所有章节（群查）
class ChapterViewSet(GenericViewSet, ListModelMixin):
    queryset = models.CourseChapter.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializer.CourseChapterSerializer

    # 基于课程分类条件下的查询
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']