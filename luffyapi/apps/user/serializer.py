# -*- coding: utf-8 -*-
# date: 2020/11/14 22:15

"""
user表字段 序列化器
"""

from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from luffyapi.utils.jwt_token import get_token


class UserSerializer(serializers.ModelSerializer):
    """
    多方式登录：用户名、手机号、邮箱
    """
    username = serializers.CharField()  # username 定义规则，单独验证

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']  # 需要用到的字段
        extra_kwargs = {  # 附加关键字参数
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    # 全局钩子校验
    def validate(self, attrs):
        from luffyapi.utils.jwt_token import get_token

        # 校验获取user对象
        user = self._get_user(attrs)
        # 签发token
        token = get_token(user)
        # 使用序列化器的context参数（dic），传递附加内容
        self.context['token'] = token
        self.context['user'] = user
        return attrs

    def _get_user(self, attrs):
        """
        1 校验手机号、邮箱、用户名
        2 返回user对象：
        """
        username = attrs.get('username')
        password = attrs.get('password')

        import re
        # 手机号校验
        if re.match('^1[3-9][0-9]{9}$', username):  # 该正则仅为示例，线上规则注需要更新
            user = models.User.objects.filter(mobile=username).first()
        # 邮箱
        elif re.match('^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()

        if user:
            ret = user.check_password(password)  # (user表继承了AbstractUser)-需密文校验
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')


class CodeUserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=True, write_only=True)
    # 手机号登录的序列化器
    code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = models.User
        fields = ['mobile', 'code']

    def validate_mobile(self, data):
        import re
        if not re.match('^1[3-9][0-9]{9}$', data):
            raise ValidationError('手机号不合法')
        return data

    def validate(self, attrs):
        mobile = self._check_code(attrs)
        user = self._get_user(mobile)
        token = get_token(user)
        self.context['token'] = token
        self.context['user'] = user
        return attrs

    def _check_code(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        # 验证码校验
        cache_code = cache.get(settings.PHONE_CACHE_KEY % mobile)
        if not code == cache_code:
            raise ValidationError('验证码错误')
        # 取出一次后，清空
        cache.set(settings.PHONE_CACHE_KEY % mobile, '', -1)
        return mobile

    def _get_user(self, mobile):
        try:
            return models.User.objects.filter(mobile=mobile).first()
        except:
            raise ValidationError('用户不存在')


class RegisterSerializer(serializers.ModelSerializer):
    """注册"""
    mobile = serializers.CharField()
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)  # 需write_only，否则会被写进数据库（无该字段报错）

    class Meta:
        model = models.User
        fields = ['mobile', 'password', 'code', 'username']
        extra_kwargs = {  # 附加关键字参数
            'password': {'min_length': 6, 'max_length': 18},
            'username': {'read_only': True}
        }

    def validate_mobile(self, data):
        import re
        if not re.match('^1[3-9][0-9]{9}$', data):
            raise ValidationError('手机号不合法')
        return data

    def validate(self, attrs):
        mobile = self._check_code(attrs)
        attrs['username'] = mobile  # 设置用户名：手机号/随机字符串
        attrs.pop('code')
        return attrs

    def _check_code(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        # 验证码校验
        cache_code = cache.get(settings.PHONE_CACHE_KEY % mobile)
        if not code == cache_code:
            raise ValidationError('验证码错误')
        # 取出一次后，清空
        # cache.set(settings.PHONE_CACHE_KEY % mobile, '', -1)
        return mobile

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.mobile = validated_data.get('mobile')
        instance.password = validated_data.get('mobile')
        ...





