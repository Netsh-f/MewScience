"""
============================
# @Time    : 2023/11/28 19:26
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from science.views.works import search_work

urlpatterns = [
    path('works', search_work),
]
