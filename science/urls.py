"""
============================
# @Time    : 2023/11/28 19:26
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from science.views.authors import search_authors
from science.views.institutions import get_institution
from science.views.works import search_works

urlpatterns = [
    path('works', search_works),
    path('authors', search_authors),
    path('institutions', get_institution),
]
