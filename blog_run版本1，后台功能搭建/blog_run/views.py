import time

from django.shortcuts import render

import constants
from article.models import Article


def index(request):
    user = request.user
    print(user)
    print(request.COOKIES)
    art = Article.objects.filter(status=constants.ARTICLE_STATUS_PASS,is_valid=True)
    return render(request,'index.html',{
        'art':art,
    })