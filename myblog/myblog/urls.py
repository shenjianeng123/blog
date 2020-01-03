"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from motangsTest.sitemaps import PostSitemap#能直接引用app肯定不是..相位寻找应该是路径

sitemaps = {'posts': PostSitemap,}

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('myblog_yangbo/', include(('myblog_yangbo.urls','myblog_yangbo'),namespace='myblog_yangbo')),
    path('blog_hxq/', include('blog_hxq.urls', namespace='blog')),
    path('blog_zhaojianbing/',include('blog_zhaojianbing.urls',namespace = 'blog_zhaojianbing')),
    path('blog/', include('blog.urls', namespace='blog')),

    path('MoTangS/',include(('motangsTest.urls','motangsTest'),namespace='MoTangSblog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
