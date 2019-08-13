from django.conf.urls import url

from article import views

urlpatterns = [
    url(r'content/(?P<uid>\S+)/$',views.Content.as_view(),name="content"),
]