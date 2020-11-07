"""junction2020 URL Configuration

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
from django.urls import path
from futureyou import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^goals/$', views.goals, name='goals'),
    url(r'^report/$', views.report, name='report'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^upload/image$', views.transactions, name='image_upload'),

    # Language url
    url(r'^lang/(?P<lang>[e]{1}[nt]{1})/$', views.set_language, name='switchlanguage')
]
