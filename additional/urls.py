"""
============================
# @Time    : 2023/11/5 20:48
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from additional.views import get_additional, transfer_additional

urlpatterns = [
    path('project', get_additional.get_project),
    path('patent', get_additional.get_patent),
    path('reward', get_additional.get_reward),
    path('reward/id', get_additional.get_reward_by_id),
    path('project/id', get_additional.get_project_by_id),
    path('patent/id', get_additional.get_patent_by_id),
    path('rewards/transfer', transfer_additional.transfer_reward),
    path('rewards/process_trans', transfer_additional.process_reward_trans),
    path('projects/transfer', transfer_additional.transfer_project),
    path('projects/process_trans', transfer_additional.process_project_trans),
    path('patents/transfer', transfer_additional.transfer_patent),
    path('patents/process_trans', transfer_additional.process_patent_trans),
]
