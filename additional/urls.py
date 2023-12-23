"""
============================
# @Time    : 2023/11/5 20:48
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from additional import views

urlpatterns = [
    path('project', views.get_project),
    path('patent', views.get_patent),
    path('reward', views.get_reward),
]
