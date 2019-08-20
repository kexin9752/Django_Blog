import uuid

from django.db import models

# Create your models here.
from django.db.models import F

import constants
from article.models import Tag


class GoodsType(models.Model):
    name = models.CharField('类型名称',max_length=32)
    code = models.CharField("编码", max_length=32, null=True, blank=True)
    description = models.CharField('类型描述',max_length=128,null=True,blank=True)
    picture = models.ImageField(verbose_name='类型图片', upload_to="goods_type",null=True,blank=True)
    reorder = models.SmallIntegerField("排序", default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name_plural = '商品标签'

    def __str__(self):
        return '{}:{}'.format(self.name, self.code)


class Goods(models.Model):
    uid = models.UUIDField("商品uid", default=uuid.uuid4, editable=True)
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_image = models.ImageField(upload_to="goods", verbose_name="商品封面图片")
    goods_count = models.IntegerField("商品库存", default=0)
    goods_number = models.IntegerField(verbose_name="商品剩余库存")
    goods_description = models.TextField(verbose_name="商品描述")
    goods_date = models.DateField(verbose_name="出厂日期")
    goods_safedate = models.IntegerField(verbose_name="保质期")
    goods_status = models.IntegerField('商品状态',choices=constants.GOODS_STATUS,default=constants.GOODS_STATUS_SELL)
    buy_link = models.CharField("购买链接", max_length=256, null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)
    reorder = models.SmallIntegerField("排序", default=0)
    view_count = models.IntegerField("浏览次数", default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    tag = models.ManyToManyField(Tag, blank=True)
    goods_type = models.ForeignKey(GoodsType,on_delete=models.CASCADE,verbose_name='商品类型')

    class Meta:
        #倒序
        ordering = ["-reorder"]
        #后台管理表名
        verbose_name_plural = '商品列表'

    def update_product_count(self,count):
        self.goods_number = F('goods_number') - count
        self.save()
        self.refresh_from_db()

    def __str__(self):
        return self.goods_name


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='goods_img')
    img = models.ImageField('商品图片',upload_to='goods_img')
    created_at = models.DateTimeField('创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = '商品图片'

    def __str__(self):
        return '商品图片'



