"""
============================
# @Time    : 2023/12/5 19:14
# @Author  : Elaikona
# @FileName: import_institutions.py
===========================
"""
import json

import requests
from django.core.management.base import BaseCommand

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id

data_folder = "/data/openalex-snapshot/data/institutions"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/institutions/_create"
headers = {'Content-Type': 'application/json'}


def institution_openAlex_to_db(data):
    institution = {key: data.get(key) for key in ['ror', 'display_name', 'country_code', 'type', 'homepage_url',
                                                  'image_url', 'works_count', 'cited_by_count', 'geo',
                                                  'associated_institutions',
                                                  'counts_by_year', 'x_concepts', 'updated_date', 'created_date',
                                                  'summary_stats']}
    institution['id'] = get_id(data.get('id'))
    return institution


def save_to_es(data):
    data_to_save = institution_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import institutions from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
