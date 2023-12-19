"""
============================
# @Time    : 2023/12/9 20:18
# @Author  : Elaikona
# @FileName: import_sources.py
===========================
"""

import json

import requests
from django.core.management.base import BaseCommand

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id

data_folder = "/data/openalex-snapshot/data/sources"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/sources/_create"
headers = {'Content-Type': 'application/json'}


def source_openAlex_to_db(data):
    source = {key: data.get(key) for key in
              ['display_name', 'host_organization', 'host_organization_name', 'works_count',
               'cited_by_count', 'summary_stats', 'homepage_url', 'country_code',
               'type', 'x_concepts', 'counts_by_year', 'updated_date', 'created_date']}
    source['id'] = get_id(data.get('id'))
    return source


def save_to_es(data):
    data_to_save = source_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import sources from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
