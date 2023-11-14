"""
============================
# @Time    : 2023/11/14 21:11
# @Author  : Elaikona
# @FileName: import_work.py
===========================
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'to import work data from openalex'

    def handle(self, *args, **kwargs):
        pass
