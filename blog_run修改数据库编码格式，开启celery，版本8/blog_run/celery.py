# import os
#
# from celery import Celery
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog_run.settings')
# app = Celery('blog_project')
# app.config_from_object('django.conf:settings')
#
# app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ================
# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_run.settings')
# app = Celery('blog_run')


# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


from __future__ import absolute_import

import os
from celery import Celery, platforms
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_run.settings')

# MySites主应用名
app = Celery('blog_run')
platforms.C_FORCE_ROOT = True

# 配置应用
app.conf.update(
    # 本地Redis服务器
    BROKER_URL=settings.BROKER_URL,
)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


