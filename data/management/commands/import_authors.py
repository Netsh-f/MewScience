"""
============================
# @Time    : 2023/12/9 19:28
# @Author  : Elaikona
# @FileName: import_authors.py
===========================
"""

import gzip
import json
import os

from django.core.management.base import BaseCommand
from django.db import DataError

from data.utils.regex_utils import get_id
from science.models import Institutions

data_folder = "H:\openalex-snapshot\data\authors"


def author_openAlex_to_db(data):
    author = {key: data.get(key) for key in ['orcid', 'display_name', 'works_count', 'cited_by_count', 'summary_stats',
                                             'last_known_institution', 'counts_by_year', 'x_concepts', 'updated_date',
                                             'created_date']}
    author['id'] = get_id(data.get('id'))
    return author
