from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from article.models import Article


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

