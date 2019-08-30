import random

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import DetailView, ListView

import constants
from accounts.models import Collect
from article.models import Article, Classify
from comment.models import CommentModel


class Content(DetailView):
    model = Article
    template_name = 'article_content.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        num = int(self.request.GET.get('num'))
        list_type = self.request.GET.get('type')
        context['num'] = num
        if num >= 0 and list_type:
            if list_type == 'index':
                art = Article.objects.filter(is_valid=True,status=constants.ARTICLE_STATUS_PASS)
            else:
                cls = get_object_or_404(Classify, code=list_type)
                art = Article.objects.filter(classify=cls,is_valid=True,status=constants.ARTICLE_STATUS_PASS)
            if num != 0:
                up_art = art[num-1]
                context['up_art'] = up_art
                context['up_num'] = num-1
            if num != art.count()-1:
                down_art = art[num+1]
                context['down_art'] = down_art
                context['down_num'] = num + 1
            context['type'] = list_type

        # 随机推荐文章，
        love_art_list = []
        art_list = Article.objects.all()
        love_num = art_list.count()
        run_count = random.choice([1,2,3,4])
        for i in range(run_count):
            random_num = random.choice(range(love_num))
            art_obj = art_list[random_num]
            love_art_list.append(art_obj)
        context['love_art_list'] = love_art_list

        # art_uid = self.object.uid
        comment = CommentModel.objects.filter(article=self.object)
        p = Paginator(comment,5)
        page_obj = p.page(1)
        context['page_obj'] = page_obj

        user = self.request.user
        is_add = None
        if user.id:
            is_add = Collect.objects.filter(article=self.object,user=user)
        context['is_add'] = is_add
        return context



def article_collect(request):
    user = request.user
    art_id = request.GET.get('id')
    art = get_object_or_404(Article,pk=art_id)
    classify = art.classify.name
    Collect.objects.create(
        user=user,
        article=art,
        classify=classify
    )
    data = {'status':1,'msg':'恭喜您,收藏成功哦耶'}
    return JsonResponse(data)


class ArticleList(ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 12

    def get_queryset(self):
        article_cls = self.request.GET.get('type')
        query = Q(is_valid=True,status=constants.ARTICLE_STATUS_PASS)
        if article_cls == 'jswz':
            cls = Classify.objects.get(code=article_cls)
            query = query & Q(classify=cls)
        elif article_cls == 'fxbj':
            cls = Classify.objects.get(code=article_cls)
            query = query & Q(classify=cls)
        elif article_cls == 'qwwz':
            cls = Classify.objects.get(code=article_cls)
            query = query & Q(classify=cls)
        elif article_cls == 'cxbc':
            cls = Classify.objects.get(code=article_cls)
            query = query & Q(classify=cls)
        return Article.objects.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article_cls = self.request.GET.get('type')
        context['type'] = '全部文章'
        if article_cls == 'jswz':
            context['type'] = '技术文章'
            context['code'] = 'jswz'
        elif article_cls == 'fxbj':
            context['type'] = '复习笔记'
            context['code'] = 'fxbj'
        elif article_cls == 'qwwz':
            context['type'] = '趣味文摘'
            context['code'] = 'qwwz'
        elif article_cls == 'cxbc':
            context['type'] = '程序报错'
            context['code'] = 'cxbc'
        return context




