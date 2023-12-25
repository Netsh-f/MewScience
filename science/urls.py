"""
============================
# @Time    : 2023/11/28 19:26
# @Author  : Elaikona
# @FileName: urls.py
===========================
"""
from django.urls import path

from science.views.authors import search_authors, get_researcher, get_related_researcher
from science.views.concepts import get_concept
from science.views.institutions import get_institution
from science.views.sources import get_hot, get_source
from science.views.works import search_works, get_work, advanced_search_works

urlpatterns = [
    path('works', search_works),
    path('authors', search_authors),
    path('institutions', get_institution),
    path('researchers', get_researcher),
    path('concepts', get_concept),
    path('work', get_work),
    path('works/advanced', advanced_search_works),
    path('hot', get_hot),
    path('researchers/related', get_related_researcher),
    path('sources', get_source),
]
