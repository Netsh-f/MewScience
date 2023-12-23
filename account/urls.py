"""
============================
# @Time    : 2023/11/5 20:48
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from account import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('self-info', views.get_self_info_view),
    path('info', views.get_info_view),
    path('set-admin', views.set_admin_view),
    path('update-intro', views.update_self_intro),
]
