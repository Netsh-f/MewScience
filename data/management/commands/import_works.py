"""
============================
# @Time    : 2023/11/21 19:35
# @Author  : Elaikona
# @FileName: import_works.py
===========================
"""
import gzip
import os
from datetime import datetime

from tqdm import tqdm

import json

import requests
from django.core.management.base import BaseCommand

from MewScience import settings
from data.utils.regex_utils import get_id

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch([settings.CONFIG['ELASTICSEARCH']['hosts']])

data_folder = "/data/openalex-snapshot/data/works"

es_url = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/works/_create"
es_url_bulk = settings.CONFIG['ELASTICSEARCH']['hosts'] + "/works/_bulk"
headers = {'Content-Type': 'application/json'}


def parse_inverted_index_to_text(abstract_inverted_index):
    if abstract_inverted_index is None:
        return None
    text = []
    for item in abstract_inverted_index:
        for index in abstract_inverted_index[item]:
            while len(text) <= index:
                text.append(None)
            text[index] = item
    text_string = ' '.join(filter(None, text))
    return text_string


def work_openAlex_to_db(data):
    work = {key: data.get(key) for key in
            ['doi', 'title', 'publication_date', 'language', 'type', 'type_crossref', 'open_access', 'authorships',
             'corresponding_institution_ids', 'cited_by_count', 'biblio', 'keywords', 'concepts', 'mesh', 'locations',
             'referenced_works', 'related_works',
             'counts_by_year', 'updated_date', 'created_date']}
    work['id'] = get_id(data.get('id'))
    work['abstract'] = parse_inverted_index_to_text(data.get('abstract_inverted_index'))
    return work


def save_to_es(data):
    data_to_save = work_openAlex_to_db(data)
    url = es_url + "/" + data_to_save['id']
    response = requests.post(url, headers=headers, data=json.dumps(data_to_save))
    if "error" in response.json():
        print(response.text)


def read_lines_bulk(path, save, month, day1, day2):
    for date_folder in os.listdir(path):
        date_folder_path = os.path.join(path, date_folder)
        if os.path.isdir(date_folder_path):
            folder_date = datetime.strptime(date_folder, "updated_date=%Y-%m-%d")
            if folder_date.month == month and day1 <= folder_date.day <= day2:
                for part_file in os.listdir(date_folder_path):
                    part_file_path = os.path.join(date_folder_path, part_file)
                    relative_path = os.path.relpath(part_file_path, path)
                    if part_file.endswith(".gz"):
                        with gzip.open(part_file_path, 'rt') as gz_file:
                            total_lines = sum(1 for line in gz_file)
                            with tqdm(total=total_lines, desc=f'Processing {relative_path}', unit=' lines') as pbar:
                                gz_file.seek(0)
                                json_data_list = []
                                for i, line in enumerate(gz_file):
                                    json_data = work_openAlex_to_db(json.loads(line))
                                    json_data['_id'] = json_data['id']
                                    json_data_list.append(json_data)
                                    pbar.update(1)
                                    if i % 50 == 0:
                                        success, failed = bulk(es, json_data_list, index="works", raise_on_error=False)
                                        if len(failed) > 0:
                                            print(failed)
                                        json_data_list = []
                                if len(json_data_list) > 0:
                                    success, failed = bulk(es, json_data_list, index="works", raise_on_error=False)


class Command(BaseCommand):
    help = 'script to import works from openalex'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, help='Specify a value for month')
        parser.add_argument('--day1', type=int, help='Specify a value for day1')
        parser.add_argument('--day2', type=int, help='Specify a value for day2')

    def handle(self, *args, **options):
        read_lines_bulk(data_folder, save_to_es, month=options['month'], day1=options['day1'], day2=options['day2'])
