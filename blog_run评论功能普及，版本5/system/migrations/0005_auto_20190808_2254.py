# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-08 22:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20190808_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoDetailModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_name', models.CharField(max_length=32, verbose_name='相片名称')),
                ('img', models.ImageField(upload_to='', verbose_name='相片')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_name', models.CharField(max_length=32, verbose_name='相册名称')),
                ('img', models.ImageField(upload_to='', verbose_name='封面图片')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='浏览次数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.AddField(
            model_name='photodetailmodel',
            name='photo_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_detail', to='system.PhotoModel'),
        ),
    ]
