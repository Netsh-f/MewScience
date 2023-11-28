# ------- Litang Save The World! -------
#
# @Time    : 2023/11/28 19:54
# @Author  : Lynx
# @File    : documents.py
#

from elasticsearch_dsl import Index
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class WorkDocument(Document):
    title = fields.TextField(attr="get_work_title")
    class Index:
        name = 'work'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}