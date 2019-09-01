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
    send_mail(subject, message, sender, receiver, html_message=html_message)



@app.task
def send_forget_password_email(to_email, username,secret_username):
    """发送激活邮件"""

    # 组织邮件信息
    subject = '欢迎回到KevIn博客'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您回到KevIn博客</h1>请点击下面链接重置您的账户密码<br/><a href="http://127.0.0.1:8000/system/password/reset/%s" style="color:blue;">点击此处连接重置密码</a>'%(username,secret_username)
    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def send_password_reset_email(to_email, username,new_password):
    """发送激活邮件"""

    # 组织邮件信息
    subject = 'KevIn博客密码修改邮件'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s, 已经为您重置密码</h1><p>您的新密码为%s<span>请及时修改，感谢您支持本博客</span></p>'%(username,new_password)
    send_mail(subject, message, sender, receiver, html_message=html_message)