from django.db import models
from luffyapi.utils.models import BaseModel


class Banner(BaseModel):
   name = models.CharField(max_length=32, verbose_name='图片名')
   img = models.ImageField(upload_to='banner', verbose_name='轮播图', help_text='图片尺寸：3840*800', null=True)
   link = models.CharField(max_length=32, verbose_name='跳转链接')
   info = models.TextField(null=True, verbose_name='图片简介')

   def __str__(self):
      return self.name
