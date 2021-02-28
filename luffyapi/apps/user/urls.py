from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.LoginView, 'login')
router.register('', views.SendSmSView, 'send')
router.register('register', views.RegisterView, 'register')  # url:/user/register/ post请求； 不写前缀，/user/ post请求


urlpatterns = [
    path('', include(router.urls)),

]
