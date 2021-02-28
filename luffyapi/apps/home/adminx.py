# -*- coding: utf-8 -*-
# date: 2020/11/12 23:29

# xadmin全局配置
import xadmin
from xadmin import views
from . import models

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "路飞学城"  # 设置站点标题
    site_footer = "路飞学城有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)

# 注册表（默认添加user表）
xadmin.site.register(models.Banner)
