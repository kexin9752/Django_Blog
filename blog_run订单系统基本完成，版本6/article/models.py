import uuid

from django.db import models

# Create your models here.
from django.db.models import F

import constants


class Tag(models.Model):
    code = models.CharField('标签编码', max_length=12,null=True,blank=True)
    name = models.CharField('标签名称',max_length=16)

    class Meta:
        verbose_name_plural = '标签列表'

    def __str__(self):
        return self.name

class Classify(models.Model):
    code = models.CharField('类型编码',max_length=12,null=True,blank=True)
    name = models.CharField('类型名称',max_length=16)

    class Meta:
        verbose_name_plural = '分类列表'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField('作者姓名',max_length=16)
    gender = models.SmallIntegerField('作者性别',choices=constants.AUTHOR_GENDER_CHOICES,default=constants.AUTHOR_GENDER_MAN)
    age = models.SmallIntegerField('作者年龄',default=0)

    class Meta:
        verbose_name_plural = '作者列表'

    def __str__(self):
        return self.name


class Article(models.Model):
    uid = models.UUIDField("文章uid",default=uuid.uuid4,editable=True)
    title = models.CharField('文章标题',max_length=64)
    content = models.TextField('文章内容')
    summary = models.CharField('文章简介',max_length=200,null=True,blank=True)
    img = models.ImageField('文章标题图片',null=True,blank=True,upload_to='%Y%m',default='/media/201907/1.jpg')
    view_count = models.PositiveIntegerField('浏览次数',default=0)
    created_at = models.DateTimeField('创建时间',auto_now_add=True)
    updated_at = models.DateTimeField('更新时间',auto_now=True)
    classify = models.ForeignKey(Classify,on_delete=models.CASCADE,related_name='classify')
    tag = models.ManyToManyField(Tag,blank=True)
    source = models.CharField('文章来源',max_length=64,null=True,blank=True)
    status = models.SmallIntegerField('文章审核',choices=constants.ARTICLE_STATUS_CHOICES,default=constants.ARTICLE_STATUS_PASS)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author')
    is_valid = models.BooleanField('是否有效',default=1)
    reorder = models.IntegerField('文章排序',default=0)
    is_top = models.BooleanField('是否置顶',default=0)
    is_best = models.BooleanField('是否推荐',default=0)

    class Meta:
        ordering = ['is_top','-is_best','-reorder','-created_at']
        verbose_name_plural = '文章列表'

    def __str__(self):
        return self.title
    # def add_view_count(self):
    #     self.view_count = F('view_count') + 1
    #     self.save(update_fields=['view_count'])

class ArticleImageModel(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_img')
    img = models.ImageField('文章图片', upload_to='%Y%m_article_img')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '文章图片'

    def __str__(self):
        return '文章图片'
