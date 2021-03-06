# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-09 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20190805_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='%Y%m_article_img', verbose_name='文章图片')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_img', to='article.Article')),
            ],
            options={
                'verbose_name_plural': '文章图片',
            },
        ),
    ]
