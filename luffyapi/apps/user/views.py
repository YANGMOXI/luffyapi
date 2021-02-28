from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from . import serializer, models
from rest_framework.decorators import action
from utils.response import APIResponse


class LoginView(ViewSet):
    # 局部禁用认证、权限组件
    # authentication_classes = ()
    # permission_classes = ()

    @action(methods=['POST'], detail=False)  # 自动生成路由
    def login(self, request, *args, **kwargs):
        """多方式登录"""
        ser = serializer.UserSerializer(data=request.data)

        if ser.is_valid():
            token = ser.context.get('token')
            username = ser.context.get('user').username

            return APIResponse(result={'token': token, 'username': username})
        else:
            return APIResponse(code=0, msg=ser.errors)

    @action(methods=['GET'], detail=False)
    def check_mobile(self, request, *args, **kwargs):
        """校验手机号是否存在"""
        import re
        mobile = request.query_params.get('mobile')
        if not re.match('^1[3-9][0-9]{9}$', mobile):  # 该正则仅为示例，线上规则注需要更新
            return APIResponse(code=0, msg='手机号不合法')
        try:
            models.User.objects.get(mobile=mobile)  # 未取到，返回None
            return APIResponse(code=1)
        except:
            return APIResponse(code=0, msg='该手机号还未注册')

    @action(methods=['POST'], detail=False)
    def code_login(self, request, *args, **kwargs):
        """验证码登录"""
        ser = serializer.CodeUserSerializer(data=request.data)

        if ser.is_valid():
            token = ser.context.get('token')
            username = ser.context.get('user').username

            return APIResponse(result={'token': token, 'username': username})
        else:
            return APIResponse(code=0, msg=ser.errors)


from .throttlings import SMSThrottling


class SendSmSView(ViewSet):
    # throttle_classes = [SMSThrottling,]

    @action(methods=['GET'], detail=False, throttle_classes=[SMSThrottling, ])
    def send(self, request, *args, **kwargs):
        """发送验证码接口"""
        import re
        from libs.tx_sms import get_code, send_message
        from libs.tx_sms import get_code, send_message
        from django.core.cache import cache
        from django.conf import settings

        mobile = request.query_params.get('mobile')
        if not re.match('^1[3-9][0-9]{9}$', mobile):
            return APIResponse(code=0, msg='手机号不合法')

        code = get_code()
        flag, errmsg = send_message(mobile, code)
        # 保存验证码（保存到cache或redis）
        # sms_cache_158332789 当缓存具有标识，防缓存冲突
        cache.set(settings.PHONE_CACHE_KEY % mobile, code, 180)

        if flag:
            return APIResponse(code=1, msg=errmsg)
        else:
            return APIResponse(code=0, msg=errmsg)


class RegisterView(GenericViewSet, CreateModelMixin):  # GenericViewSet不需要重写update、create等方法
    """注册（手机号）"""
    queryset = models.User.objects.all()
    serializer_class = serializer.RegisterSerializer

    # 写法一
    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            username = ser.data.get('username')
            return APIResponse(code=1, msg='注册成功', result={'username': username})
        else:
            return APIResponse(code=0, msg=ser.errors)

    # 写法二（重写）
    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     username = response.data.get('username')
    #     return APIResponse(code=1, msg='注册成功', username=username)
