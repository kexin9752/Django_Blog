from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'user/login/$',views.user_login,name="user_login"),
    url(r'user/logout/$',views.user_logout,name="user_logout"),
    url(r'user/register/$',views.user_register,name="user_register"),
    url(r'verify/code/$',views.verify_code,name="verify_code"),
    url(r'user/center/index/$',views.user_center_index,name="user_center_index"),
    url(r'user/center/proinfo/$',views.user_center_proinfo,name="user_center_proinfo"),
    url(r'user/center/password/$',views.user_center_password,name="user_center_password"),
    url(r'user/center/convert/$',views.user_point_convert,name="user_point_convert"),
    url(r'user/center/list/$',views.user_point_list,name="user_point_list"),
]