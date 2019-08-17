import uuid

from django.db import models

# Create your models here.
from article.models import Article


# class BaseModel(models.Model):
#     user_id = models.IntegerField('评论用户ID',null=True,blank=True)
#     nickname = models.CharField('评论昵称',max_length=64)
#     content = models.TextField('评论', max_length=500)
#     tel = models.CharField('评论电话',max_length=16,null=True,blank=True)
#     qq = models.CharField('评论QQ',max_length=16,null=True,blank=True)
#     email = models.EmailField('邮箱',null=True,blank=True)
#     time = models.DateTimeField('评论时间',auto_now_add=True)
#     address = models.CharField('用户地址',max_length=125,default='未知')
#
#
#     class Meta:
#         abstract = True
#
#
# class ArticleComment(BaseModel):
#     # article = models.CharField('文章uid',max_length=245,null=True,blank=True)
#     article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',verbose_name='评论文章',null=True, blank=True)
#     note_id = models.IntegerField('随笔id',null=True,blank=True)
#     level_msg_id = models.IntegerField('留言id',null=True,blank=True)
#     photo = models.IntegerField('相册id', null=True, blank=True)
#     mall = models.IntegerField('素材id', null=True, blank=True)
#
#
#     class Meta:
#         ordering = ['-time']
#
#
# class ArticleCommentReply(BaseModel):
#     comment = models.ForeignKey(ArticleComment,on_delete=models.CASCADE,related_name='replied',verbose_name='一级评论')
#     reply = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,verbose_name='回复对象')


class CommentModel(models.Model):
    user_id = models.IntegerField('评论用户ID',null=True,blank=True,default=0)
    u_name = models.CharField('评论昵称',max_length=64)
    u_code = models.UUIDField("用户uid",default=uuid.uuid4,editable=True)
    u_mail = models.EmailField('邮箱',null=True,blank=True)
    mycity = models.CharField('用户地址',max_length=125,default='未知')
    u_url = models.CharField('用户导航',max_length=225,null=True,blank=True)
    txtContent = models.TextField('评论', max_length=500)
    img = models.CharField('用户头像',max_length=32,default='6')
    art_uid = models.CharField('文章uid',max_length=225,null=True,blank=True)
    note_id = models.IntegerField('随笔id',null=True,blank=True)
    level_msg_id = models.IntegerField('随笔id',null=True,blank=True)
    photo_id = models.IntegerField('随笔id',null=True,blank=True)
    mall_id = models.IntegerField('随笔id',null=True,blank=True)
    qq = models.CharField('评论QQ',max_length=16,null=True,blank=True)
    tel = models.CharField('评论电话',max_length=16,null=True,blank=True)
    created_at = models.DateTimeField('评论时间',auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ReCommentModel(models.Model):
    comment = models.ForeignKey(CommentModel,on_delete=models.CASCADE,related_name='recomment',verbose_name='子评论',null=True,blank=True)
    self_reply = models.ForeignKey('self',null=True,blank=True)
    u_name = models.CharField('评论昵称',max_length=64)
    u_code = models.UUIDField("用户uid",default=uuid.uuid4,editable=True)
    to_code = models.UUIDField('对方用户uid',editable=True,null=True,blank=True)
    to_recode = models.UUIDField('子评论中对方用户uid', editable=True, null=True, blank=True)
    txtContent = models.TextField('评论', max_length=500)
    img = models.CharField('用户头像',max_length=32,default='7')
    created_at = models.DateTimeField('评论时间',auto_now_add=True)

    class Meta:
        ordering = ['-created_at']




