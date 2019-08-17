from django.db import models

# Create your models here.
from django.db.models import F


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



