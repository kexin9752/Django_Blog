from django.conf.urls import url

from system import views

urlpatterns = [
    url(r'about/me/$',views.about_me,name="about_me"),
    url(r'write/some/$',views.WriteSome.as_view(),name="write_some"),
    url(r'write/content/(?P<pk>\S+)/$', views.WriteContent.as_view(), name="write_content"),
]

