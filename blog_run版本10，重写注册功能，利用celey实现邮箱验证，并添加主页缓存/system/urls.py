from django.conf.urls import url

from system import views

urlpatterns = [
    url(r'about/me/$',views.about_me,name="about_me"),
    url(r'write/some/$',views.WriteSome.as_view(),name="write_some"),
    url(r'write/content/(?P<pk>\S+)/$', views.WriteContent.as_view(), name="write_content"),
    url(r'feed/back/$',views.FeedBack.as_view(),name="feed_back"),
    url(r'link/$',views.LinkView.as_view(),name="link"),
    url(r'photo/$',views.PhotoList.as_view(),name="photo"),
    url(r'photo/detail/$', views.PhotoDetail.as_view(), name="photo_detail"),
]

