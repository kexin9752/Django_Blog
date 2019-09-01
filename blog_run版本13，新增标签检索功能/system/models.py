import uuid

from django.db import models

# Create your models here.
from django.db.models import F

import constants
from accounts.models import User
from article.models import Tag, Classify


class UserWrite(models.Model):
    name = models.CharField('管理员',max_length=32,default='KevIn')
    address = models.CharField('目前所在',max_length=64,default='北京市朝阳区')
    content = models.TextField('随笔内容')
    img = models.ImageField('随笔图片',upload_to='write_some',null=True,blank=True)
    created_at = models.DateTimeField('创建时间',auto_now_add=True)
    view_count = models.PositiveIntegerField('浏览次数',default=0)

    class Meta:
        ordering = ['created_at']

    def increase_view_count(self):
        self.view_count = F('view_count') + 1
        self.save()
        self.refresh_from_db()


class LinkModel(models.Model):
    web_name = models.CharField('网站名称',max_length=120)
    contact_man = models.CharField('联系人',max_length=64)
    phone = models.CharField('联系电话',max_length=11,null=True,blank=True)
    email = models.EmailField('邮箱',max_length=120,null=True,blank=True)
    web_link = models.URLField('网站网址',max_length=200)
    web_description = models.TextField('网站描述',max_length=500)
    status = models.SmallIntegerField('申请状态',choices=constants.WEB_LINK_STATUS_CHOICES,default=constants.WEB_LINK_WAIT)
    is_inner = models.BooleanField('是否为内连接',default=False)

    created_at = models.DateTimeField('创建时间',auto_now_add=True)
    updated_at = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        ordering = ['-created_at','-updated_at']
        verbose_name_plural = '友情链接'


class PhotoModel(models.Model):
    photo_name = models.CharField('相册名称',max_length=32)
    img = models.ImageField('封面图片',upload_to='photo')
    view_count = models.PositiveIntegerField('浏览次数',default=0,editable=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '相册'

    def __str__(self):
        return self.photo_name


class PhotoDetailModel(models.Model):
    photo_obj = models.ForeignKey(PhotoModel,on_delete=models.CASCADE,related_name='photo_detail')
    photo_name = models.CharField('相片名称',max_length=32)
    img = models.ImageField('相片',upload_to='photo_detail')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '相片集合'

    def __str__(self):
        return self.photo_name


class Slider(models.Model):
    name = models.CharField("名称",max_length=32)
    desc = models.CharField("描述",max_length=100,null=True,blank=True)
    types = models.SmallIntegerField("展示位置",choices=constants.SLIDER_TYPES_CHOICES,
                                     default=constants.SLIDER_TYPE_INDEX)
    img = models.ImageField('图片',upload_to='slider')
    reorder = models.SmallIntegerField("排序",default=0,help_text='数字越大越靠前')
    start_time = models.DateTimeField("生效时间",null=True,blank=True)
    end_time = models.DateTimeField("结束时间",null=True,blank=True)
    target_url = models.CharField("跳转地址",max_length=256,null=True,blank=True)
    is_valid = models.BooleanField("是否生效",default=True)
    created_at = models.DateTimeField("创建时间",auto_now_add=True)
    updated_at = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = 'system_slider'
        ordering = ['-reorder']
        verbose_name_plural = '轮播图列表'


class VideoType(models.Model):
    name = models.CharField('视频类型名称',max_length=12)
    code = models.CharField('视频类型编码',max_length=6)

    class Meta:
        verbose_name_plural = '视频类型'

    def __str__(self):
        return self.name


class VideoModel(models.Model):
    user = models.ForeignKey(to=User,related_name='video')
    uid = models.UUIDField("视频uid",default=uuid.uuid4,editable=True)
    title = models.CharField('视频标题',max_length=24)
    video = models.CharField('视频地址',max_length=255)
    img = models.ImageField('视频封面图片', null=True, blank=True, upload_to='video', default='video/1.jpg')
    view_count = models.IntegerField('浏览次数',default=0)
    desc = models.TextField('视频描述',max_length=600)
    tag = models.ManyToManyField(Tag,blank=True)
    classify = models.ForeignKey(VideoType,null=True,blank=True)
    is_best = models.BooleanField('是否推荐',default=False)
    is_valid = models.BooleanField('是否有效', default=1)
    reorder = models.IntegerField('视频排序', default=0)
    is_top = models.BooleanField('是否置顶', default=0)
    source = models.CharField('视频来源', max_length=64, null=True, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['is_top','is_best','-reorder']
        verbose_name_plural = '我的视频'