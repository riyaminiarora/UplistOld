"""prouplistold URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import  views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('signup', views.signup,name='signup'),
    path('', views.home,name='home'),
    path('signin', views.signin,name='signin'),
    path('signout', views.signout,name='signout'),
    path('profile', views.profile,name='profile'),
    path('myads', views.myads,name='myads'),
    path('inbox', views.inbox,name='inbox'),
    path('outbox', views.outbox,name='outbox'),
    path('adpost', views.postad,name='postad'),
    path('editpost/<int:id>', views.editad,name='editad'),
    path('delad/<int:id>', views.ad_delete,name='ad_delete'),
    path('changepass', views.changepass,name='changepass'),
    path('sendmessage/<int:id>', views.sendmessage,name='sendmessage'),
    path('detail/<int:id>', views.addetail,name='detail'),
    path('adsbycat/<int:id>', views.adsbycat,name='adsbycat'),
]
