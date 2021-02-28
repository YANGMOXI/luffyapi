# -*- coding: utf-8 -*-
# date: 2020/12/4 10:44


from rest_framework import serializers
from . import models


# 课程分类
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


# 讲师
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['name', 'role_name', 'title']


# 课程
class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化
    teacher = TeacherSerializer()
    section_list = serializers.ListField()

    class Meta:
        model = models.Course
        fields = ['id',
                  'name',
                  'course_img',
                  'brief',
                  'attachment_path',
                  'pub_sections',
                  'price',
                  'students',
                  'period',
                  'sections',
                  'course_type_name',
                  'level_name',
                  'status_name',
                  'teacher',
                  'section_list',
                  ]


# 子序列化器 - 课时
class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = ('name', 'orders', 'section_link', 'duration', 'free_trail')

# 课程章节
class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseSectionSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ('name', 'chapter', 'summary', 'coursesections')
