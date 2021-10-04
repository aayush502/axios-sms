"""axios_sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from sms_consumer.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/$', SmsLog.as_view(), name="log"),
    url(r'^count/', ConsumerList.as_view(), name="count"),
    path("countupdate/<int:id>/", ConsumerUpdate.as_view(), name="count-update"),
    url(r'^register/', UserRegister.as_view(), name="register"),
    url(r'^login/', UserLogin.as_view(), name="login"),
    url(r'^logout/', logout, name="logout"),
    url(r'^home/', Home.as_view(), name="home"),
    path("select2/", include("django_select2.urls")),
]
