# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-01 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='before_ip',
            field=models.CharField(default='暂无记录', max_length=64, verbose_name='用户上次IP'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ip',
            field=models.CharField(default='暂无记录', max_length=64, verbose_name='用户本次IP'),
        ),
    ]
