# from __future__ import absolute_import
# from blog_run.celery import app
#
# import time
#
# @app.task
# def test(a,b):
#       print('任务开始')
#       time.sleep(5)
#       print(a+b)
#       print('任务结束')

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# import time
#
# from accounts.models import User
# from blog_run.celery import app
#
#
# @app.task
# def add(x, y):
#     return x + y
#
#
# @app.task
# def run_test_suit(ts_id):
#     time.sleep(10)
#     User.objects.filter(is_fresh=0).update(is_fresh=1)
#     return 'ok'




from __future__ import absolute_import
from blog_run.celery import app
from celery import task, shared_task


@app.task
def start_running(info):
    print(info)
    print('--->>开始执行任务<<---')
    print('比如发送短信或邮件')
    print('>---任务结束---<')


@task
def pushMsg(uid,msg):
    print('推送消息',uid,msg)
    return True

@shared_task
def add(x,y):
    print('加法：',x + y)
    return x + y


@shared_task
def mul(x, y):
    print('乘法',x*y)
    return x * y
