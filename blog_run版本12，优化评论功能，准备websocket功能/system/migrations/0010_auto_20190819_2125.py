# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-19 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_auto_20190819_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videomodel',
            options={'ordering': ['is_top', 'is_best', '-reorder'], 'verbose_name_plural': '我的视频'},
        ),
    ]
