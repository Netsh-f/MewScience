"""
============================
# @Time    : 2023/11/14 21:11
# @Author  : Elaikona
# @FileName: import_work.py
===========================
"""
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'to import work data from openalex'

    def handle(self, *args, **kwargs):
        print("---test---")
        # api = "https://api.openalex.org/works?per-page=50&page=1&filter=cited_by_count:%3E1000"
        # response = requests.get(api)
        # print(response.json())
        pass
