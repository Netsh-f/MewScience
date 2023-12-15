"""
============================
# @Time    : 2023/12/9 19:28
# @Author  : Elaikona
# @FileName: import_authors.py
===========================
"""
import json
import os

import requests
from django.core.management.base import BaseCommand
from django.db import DataError, IntegrityError

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id
from science.models import Authors

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

data_folder = "E:\openalex-snapshot\data\\authors"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/authors/_create"
headers = {'Content-Type': 'application/json'}
auth_str = settings.CONFIG['ELASTICSEARCH']['http_auth']
auth = tuple(eval(auth_str))


def author_openAlex_to_db(data):
    author = {key: data.get(key) for key in ['orcid', 'display_name', 'works_count', 'cited_by_count', 'summary_stats',
                                             'last_known_institution', 'counts_by_year', 'x_concepts', 'updated_date',
                                             'created_date']}
    author['id'] = get_id(data.get('id'))
    return author


def save_to_database(data):
    concept = author_openAlex_to_db(data)
    try:
        Authors.objects.create(**concept)
    except (DataError, IntegrityError):
        pass


def save_to_es(data):
    data_to_save = author_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save), auth=auth, verify=False)
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import authors from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
