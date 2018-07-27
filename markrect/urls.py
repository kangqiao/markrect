"""markrect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView
from cmds.views import *
import xadmin

schema_view = get_swagger_view(title="藏经标注平台API")

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('backend/', admin.site.urls),
    path('manage/', xadmin.site.urls),
    url(r'^auth/', include("jwt_auth.urls", namespace="api-auth")),
    url(r'^api/', include('api.urls')),
    path('cmds/cutfixed_pages/', cutfixed_pages, name='cutfixed_pages'),
    path('cmds/cutfixed_pages/<pid>/', cutfixed_page_detail, name='cutfixed_page_detail'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r"^docs/$", schema_view),
]

# # 通用URL映射，必须放在最后
urlpatterns += [
    # 通用页面URL映射，必须放在最后
    #url(r'^api/v1', include('api.urls', namespace='api')),
]
