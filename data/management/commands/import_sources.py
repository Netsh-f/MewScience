"""
============================
# @Time    : 2023/12/9 20:18
# @Author  : Elaikona
# @FileName: import_sources.py
===========================
"""

from django.core.management.base import BaseCommand
from django.db import DataError

from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id
from science.models import Sources

data_folder = "E:\openalex-snapshot\data\sources"


def source_openAlex_to_db(data):
    source = {key: data.get(key) for key in
              ['display_name', 'host_organization', 'host_organization_name', 'works_count',
               'cited_by_count', 'summary_stats', 'homepage_url', 'country_code',
               'type', 'x_concepts', 'counts_by_year', 'updated_date', 'created_date']}
    source['id'] = get_id(data.get('id'))
    return source


def save_to_database(data):
    source = concept_openAlex_to_db(data)
    try:
        Sources.objects.create(**source)
    except DataError:
        print("drop one line")


class Command(BaseCommand):
    help = 'script to import sources from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_database)
