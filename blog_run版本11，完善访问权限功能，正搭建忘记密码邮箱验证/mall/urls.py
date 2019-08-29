from django.conf.urls import url

from mall import views

urlpatterns = [
    url(r'down/$',views.DownView.as_view(),name="down"),
    url(r'down/content/(?P<uid>\S+)/$', views.DownContent.as_view(), name="down_content"),
    url(r'goods/shopping/$',views.goods_shopping,name="goods_shopping"),
    # url(r'')
]



