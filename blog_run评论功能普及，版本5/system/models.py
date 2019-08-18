from django.db import models

# Create your models here.
from django.db.models import F

import constants


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



