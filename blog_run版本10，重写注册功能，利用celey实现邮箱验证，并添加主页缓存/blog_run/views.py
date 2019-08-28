import time

from django.shortcuts import render

import constants
from accounts.models import Order
from article.models import Article, Tag
from comment.models import CommentModel
from mall.models import Goods
from system.models import UserWrite, LinkModel

#侧边栏和底边栏到时候用接口写
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)
def index(request):
    user = request.user
    goods = Goods.objects.filter(goods_status=constants.GOODS_STATUS_SELL,is_valid=True)[:3]
    art = Article.objects.filter(status=constants.ARTICLE_STATUS_PASS,is_valid=True)
    return render(request,'index.html',{
        'art':art,
        'goods':goods,
    })



