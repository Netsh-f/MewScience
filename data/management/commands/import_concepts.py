"""
============================
# @Time    : 2023/12/9 19:53
# @Author  : Elaikona
# @FileName: import_concepts.py
===========================
"""

from django.core.management.base import BaseCommand
from django.db import DataError

from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id
from science.models import Concepts

data_folder = "E:\openalex-snapshot\data\concepts"


def concept_openAlex_to_db(data):
    concept = {key: data.get(key) for key in
               ['display_name', 'level', 'description', 'works_count', 'cited_by_count', 'summary_stats', 'image_url',
                'ancestors', 'related_concepts', 'counts_by_year', 'updated_date', 'created_date']}
    concept['id'] = get_id(data.get('id'))
    return concept


def save_to_database(data):
    concept = concept_openAlex_to_db(data)
    try:
        Concepts.objects.create(**concept)
    except DataError:
        pass


class Command(BaseCommand):
    help = 'script to import concepts from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_database)
