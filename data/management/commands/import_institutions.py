"""
============================
# @Time    : 2023/12/5 19:14
# @Author  : Elaikona
# @FileName: import_institutions.py
===========================
"""
import gzip
import json
import os

from django.core.management.base import BaseCommand
from django.db import DataError

from data.utils.regex_utils import get_id
from science.models import Institutions

data_folder = "H:\openalex-snapshot\data\institutions"


def save_to_database(data):
    institutions = {key: data.get(key) for key in ['ror', 'display_name', 'country_code', 'type', 'homepage_url',
                                                   'image_url', 'works_count', 'cited_by_count', 'geo',
                                                   'associated_institutions',
                                                   'counts_by_year', 'x_concepts', 'updated_date', 'created_date',
                                                   'summary_stats']}
    institutions['id'] = get_id(data.get('id'))
    try:
        Institutions.objects.create(**institutions)
    except DataError:
        print("drop one line")


class Command(BaseCommand):
    help = 'script to import institutions from openalex'

    def handle(self, *args, **options):
        for date_folder in os.listdir(data_folder):
            date_folder_path = os.path.join(data_folder, date_folder)

            # 检查是否为文件夹
            if os.path.isdir(date_folder_path):
                print(f"---import {date_folder_path}")

                # 遍历每个日期文件夹下的part文件
                for part_file in os.listdir(date_folder_path):
                    part_file_path = os.path.join(date_folder_path, part_file)

                    # 检查是否为gzip文件
                    if part_file.endswith(".gz"):
                        print(f"import {part_file_path}")

                        # 打开gzip文件并读取内容
                        with gzip.open(part_file_path, 'rt') as gz_file:
                            # 逐行读取JSON数据
                            for line in gz_file:
                                json_data = json.loads(line)
                                save_to_database(json_data)
                        print(f"import {part_file_path} completed")
                print(f"---import {date_folder_path} completed")
