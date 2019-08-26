import time

from django.shortcuts import render

import constants
from accounts.models import Order
from article.models import Article, Tag
from comment.models import CommentModel
from mall.models import Goods
from system.models import UserWrite, LinkModel

#侧边栏和底边栏到时候用接口写
def index(request):
    user = request.user
    goods = Goods.objects.filter(goods_status=constants.GOODS_STATUS_SELL,is_valid=True)[:3]
    art = Article.objects.filter(status=constants.ARTICLE_STATUS_PASS,is_valid=True)
    art_best = Article.objects.filter(status=constants.ARTICLE_STATUS_PASS,is_best=True, is_valid=True)[:3]
    new_art = art.order_by('-created_at').first()
    rank_art = art.order_by('-view_count')[:6]
    user_write = UserWrite.objects.order_by('-view_count')[:3]
    tags = Tag.objects.all()[:30]
    note_list = CommentModel.objects.filter(note_id=1)[:3]
    link_list = LinkModel.objects.filter(status=constants.WEB_LINK_PASS)
    return render(request,'index.html',{
        'art':art,
        'goods':goods,
        'new_art':new_art,
        'user_write':user_write,
        'art_best':art_best,
        'tags':tags,
        'note_list': note_list,
        'rank_art':rank_art,
    })



