"""picha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.MainView.as_view(),name='index'),
    url(r'^photo/$',views.ProcessView.as_view(), name='photo'),
    url(r'^photos/$',views.Photos.as_view(), name='photos'),
    url(r'^photo/(?P<pk>[0-9]+)/$',views.PicView.as_view(), name='picdetails'),
    url(r'^preset/([\w-]+)/([0-9]+)/$',views.Effects.as_view(), name='preset'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

