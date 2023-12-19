"""
============================
# @Time    : 2023/12/9 19:28
# @Author  : Elaikona
# @FileName: import_authors.py
===========================
"""
import json

import requests
from django.core.management.base import BaseCommand

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data, read_lines
from data.utils.regex_utils import get_id

data_folder = "/data/openalex-snapshot/data/authors"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/authors/_create"
headers = {'Content-Type': 'application/json'}


def author_openAlex_to_db(data):
    author = {key: data.get(key) for key in ['orcid', 'display_name', 'works_count', 'cited_by_count', 'summary_stats',
                                             'last_known_institution', 'counts_by_year', 'x_concepts', 'updated_date',
                                             'created_date']}
    author['id'] = get_id(data.get('id'))
    return author


def save_to_es(data):
    data_to_save = author_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    requests.post(url, headers=headers, data=json.dumps(data_to_save))


class Command(BaseCommand):
    help = 'script to import authors from openalex'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, help='Specify a value for month')
        parser.add_argument('--day1', type=int, help='Specify a value for day1')
        parser.add_argument('--day2', type=int, help='Specify a value for day2')

    def handle(self, *args, **options):
        read_lines(data_folder, save_to_es, month=options['month'], day1=options['day1'], day2=options['day2'])
