"""
============================
# @Time    : 2023/11/5 20:48
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from additional import views
from additional.views import get_reward_by_id, get_project_by_id, get_patent_by_id

urlpatterns = [
    path('project', views.get_project),
    path('patent', views.get_patent),
    path('reward', views.get_reward),
    path('reward/id', get_reward_by_id),
    path('project/id', get_project_by_id),
    path('patent/id', get_patent_by_id),
]
