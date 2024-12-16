# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import settings


class WeChatConfig(AppConfig):
    name = "wechat_django"
    verbose_name = _("WeChat")
    verbose_name_plural = _("WeChat")

    def ready(self):
        import object_tool
        object_tool.ObjectToolConfig.register()

        if settings.PATCHADMINSITE:
            from .sites.admin import patch_admin
            patch_admin()

        admin.site.final_catch_all_view = False

        # 注册注册关注,取关事件
        from . import signals
        from .handler import handle_subscribe_events

        signals.message_received.connect(handle_subscribe_events)
