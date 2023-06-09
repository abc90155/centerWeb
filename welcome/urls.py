"""centerWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name="welcome"),
    path('', RedirectView.as_view(url='chat/')),
    path('chat', views.chatPage, name = 'chat'),
    path('chat/<int:pk>/', chatDetail.as_view(), name='chatDetails'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_view, name='logout'),    
    path('signup/',views.signup, name='signup'),    
    path('settings/',views.settings, name='settings'),
    path('talking/',views.talking, name='talking'),
    path('admin_home/',views.admin_home, name='admin_home'),    
    path('delete_chat/',views.delete_chat, name='del_chat'),


]
