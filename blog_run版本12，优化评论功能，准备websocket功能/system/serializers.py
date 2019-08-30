from rest_framework import serializers

from article.models import Article, Tag
from comment.models import CommentModel
from mall.models import Goods
from system.models import UserWrite, LinkModel


class ArticleBestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Article
        fields = ['uid','title','content','img','view_count','created_at','is_best','status','reorder']


class UserWriteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserWrite
        fields = ['name', 'content', 'created_at','view_count']



class NoteMsgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CommentModel
        fields = ['u_name', 'txtContent', 'img', 'created_at']


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class LinkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = LinkModel
        fields = ['web_link','web_name']


class GoodsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Goods
        fields = ['uid','goods_name','view_count']

