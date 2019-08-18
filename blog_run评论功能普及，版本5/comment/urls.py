from django.conf.urls import url

from comment import views

urlpatterns = [
    url(r'comment/$',views.CommentView.as_view(),name="comment"),
    url(r'comment/load/$', views.CommentLoad.as_view(), name="comment_load"),
]