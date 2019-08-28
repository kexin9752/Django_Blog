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

import time

from django.conf import settings

from accounts.models import User
from blog_run.celery import app
from celery import task, shared_task


# @app.task
# def start_running(info):
#     print(info)
#     print('--->>开始执行任务<<---')
#     print('比如发送短信或邮件')
#     print('>---任务结束---<')
#
#
# @task
# def pushMsg(uid,msg):
#     print('推送消息',uid,msg)
#     return True
#
# @shared_task
# def add(x,y):
#     print('加法：',x + y)
#     return x + y


# @app.task(name='tasks.mul')
# def mul(x, y):
#     print('乘法',x*y)
#     return x * y

from django.core.mail import send_mail

@app.task(name='tasks.fresh_user')
def fresh_user():
    User.objects.filter(is_fresh=False).update(is_fresh=True)
    return '用户状态刷新完成'


@app.task
def email_send(email):
    time.sleep(10)
    print('发送邮件',email)
    return '已发送'


@app.task
def send_activate_email(to_email, username, token):
    """发送激活邮件"""

    # 组织邮件信息
    subject = '欢迎注册KevIn博客'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您注册KevIn博客</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/accounts/user/email/verify/%s">http://127.0.0.1:8000/mail/activate/%s</a>'%(username, token, token)
    time.sleep(5)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)