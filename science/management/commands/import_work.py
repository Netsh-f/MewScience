"""
============================
# @Time    : 2023/11/14 21:11
# @Author  : Elaikona
# @FileName: import_work.py
===========================
"""
import requests
from django.core.management.base import BaseCommand

from science.models import Work


class Command(BaseCommand):
    help = 'to import work data from openalex'

    def handle(self, *args, **kwargs):
        for i in range(2, 4):
            api = "https://api.openalex.org/works?per-page=100&page=" + str(i) + "&filter=concept.id:C41008148"
            response = requests.get(api).json()
            results = response['results']
            for result in results:
                Work.objects.create(data=result)
            print(f"page {i} import finished")
