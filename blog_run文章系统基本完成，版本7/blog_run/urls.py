"""blog_run URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from xadmin.plugins import xversion
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
# from django.urls import path

from blog_run import views


# router = routers.DefaultRouter
# router.routes(r'integral',UserIntegralViewSet)
xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    # url('admin/', admin.site.urls),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^$',views.index,name='index'),
    url(r'^article/',include('article.urls',namespace='article')),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    url(r'^system/',include('system.urls',namespace='system')),
    url(r'^comment/',include('comment.urls',namespace='comment')),
    url(r'^mall/',include('mall.urls',namespace='mall')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)