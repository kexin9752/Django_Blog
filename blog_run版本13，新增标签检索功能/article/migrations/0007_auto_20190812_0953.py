# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-12 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20190811_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(blank=True, default='201907/1.jpg', null=True, upload_to='%Y%m', verbose_name='文章标题图片'),
        ),
    ]
