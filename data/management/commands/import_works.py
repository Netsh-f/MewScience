"""
============================
# @Time    : 2023/11/21 19:35
# @Author  : Elaikona
# @FileName: import_works.py
===========================
"""
from django.core.management.base import BaseCommand
from django.db import DataError

from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id
from science.models import Works

data_folder = "E:\openalex-snapshot\data\works"


def work_openAlex_to_db(data):
    work = {key: data.get(key) for key in
            ['title', 'publication_date', 'language', 'type', 'authors',
             'cited_by_count', 'biblio', 'keywords', 'x_concepts', 'locations',
             'referenced_works', 'related_works', 'abstract_inverted_index',
             'counts_by_year', 'updated_date', 'created_date']}
    work['id'] = get_id(data.get('id'))
    return work


def save_to_database(data):
    concept = work_openAlex_to_db(data)
    try:
        Works.objects.create(**concept)
    except DataError:
        pass


class Command(BaseCommand):
    help = 'script to import works from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_database)
