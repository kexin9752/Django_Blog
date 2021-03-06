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
    url(r'forget/password/$',views.forget_password,name="forget_password"),
    url(r'password/reset/(?P<secret_username>\S+)/$',views.password_reset,name="password_reset"),
    url(r'music/$',views.MusicView.as_view(),name="music"),
    url(r'video/list/$',views.VideoList.as_view(),name="video_list"),
    url(r'video/show/(?P<uid>\S+)/$',views.VideoShow.as_view(),name="video_show"),
    url(r'tag/list/$',views.TagList.as_view(),name="tag_list"),

    url(r'cktest/$',views.cktest,name="cktest"),
    # url(r'web_test/$', views.web_test),
    # url(r'path/$', views.path),
]

