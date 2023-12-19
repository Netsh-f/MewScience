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
from data.utils.reader import read_lines_from_openalex_data
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
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import authors from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
