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

import json

import requests
from django.core.management.base import BaseCommand

from MewScience import settings
from data.utils.reader import read_lines_from_openalex_data
from data.utils.regex_utils import get_id

data_folder = "/data/openalex-snapshot/data/works"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/works/_create"
headers = {'Content-Type': 'application/json'}


def work_openAlex_to_db(data):
    work = {key: data.get(key) for key in
            ['title', 'publication_date', 'language', 'type', 'authors',
             'cited_by_count', 'biblio', 'keywords', 'x_concepts', 'locations',
             'referenced_works', 'related_works', 'abstract_inverted_index',
             'counts_by_year', 'updated_date', 'created_date']}
    work['id'] = get_id(data.get('id'))
    return work


def save_to_es(data):
    data_to_save = work_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


class Command(BaseCommand):
    help = 'script to import works from openalex'

    def handle(self, *args, **options):
        read_lines_from_openalex_data(data_folder, save_to_es)
