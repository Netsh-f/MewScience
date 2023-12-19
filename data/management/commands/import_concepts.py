"""
============================
# @Time    : 2023/12/9 19:53
# @Author  : Elaikona
# @FileName: import_concepts.py
===========================
"""
import json

import requests
from django.core.management.base import BaseCommand
from django.db import DataError

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id
from science.models import Concepts

data_folder = "/data/openalex-snapshot/data/concepts"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/concepts/_create"
headers = {'Content-Type': 'application/json'}
auth_str = settings.CONFIG['ELASTICSEARCH']['http_auth']
auth = tuple(eval(auth_str))

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def save_to_es(data):
    data_to_save = concept_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import concepts from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
