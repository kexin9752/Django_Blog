from django.conf.urls import url

from article import views

urlpatterns = [
    url(r'content/(?P<uid>\S+)/$',views.Content.as_view(),name="content"),
    url(r'article/collect/$',views.article_collect,name="article_collect"),
    url(r'article/list/$', views.ArticleList.as_view(), name="article_list"),
]