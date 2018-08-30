"""Recruitment_Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from  django.conf.urls import  url,include
from django.conf import  settings
from Condidate import  views as condidatesViews
from accounts import  views as accountsViews
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^recruitment',condidatesViews.home,name='Home'),
    url(r'^candidates/apply/$', condidatesViews.apply, name='candidate_apply'),
    url(r'^candidates/apply/success/$', condidatesViews.apply_success, name='candidate_apply_success'),
    url(r'^login',accountsViews.userlogin,name='login'),
    url(r'^detail/(?P<id_num>\d+)/$', condidatesViews.detail, name='detail'),

]
