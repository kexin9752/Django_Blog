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
    url(r'user/center/list/$',views.UserIntegralList.as_view(),name="user_point_list"),
    url(r'user/integral/del/$',views.user_integral_del,name="user_integral_del"),
    url(r'user/center/recharge/$',views.UserRecharge.as_view(),name="user_center_recharge"),
    url(r'user/amount/log/$',views.UserBalanceView.as_view(),name="user_amount_log"),
    url(r'user/balance/del',views.UserBalanceDel.as_view(),name="user_balance_del"),
    url(r'user/balance/list',views.user_balance_list,name="user_balance_list"),
    url(r'user/collect/$',views.UserCollectView.as_view(),name="user_collect"),
    url(r'user/collect/del/$',views.UserCollectDel.as_view(),name="user_collect_del"),
    url(r'user/center/avatar/$',views.user_center_avatar,name="user_center_avatar"),
    url(r'user/message/add/$',views.UserMessageAdd.as_view(),name="user_message_add"),
    url(r'user/message/accept/list/$',views.UserMessageList.as_view(),name="user_message_accept_list"),
    url(r'user/message/send/list/$',views.UserMessageList.as_view(template_name='user_manage/user_message_send.html'),name="user_message_send_list"),
    url(r'user/message/system/list/$',views.UserMessageList.as_view(template_name='user_manage/user_message_system.html'),name="user_message_system_list"),
    url(r'user/message/del/$',views.UserMessageDel.as_view(),name="user_message_del"),
    url(r'user/message/accept/del/$', views.UserMessageAcceptDel.as_view(), name="user_message_accept_del"),
    url(r'user/message/detail/(?P<pk>\S+)$', views.UserMessageDetail.as_view(), name="user_message_detail"),
    url(r'user/message/accept/detail/(?P<pk>\S+)$', views.UserMessageAcceptDetail.as_view(), name="user_message_accept_detail"),

]