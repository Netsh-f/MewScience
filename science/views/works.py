"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""
from elasticsearch_dsl import Q
from rest_framework.decorators import api_view

from science.documents import WorkDocument
from science.models import Works
from science.request_serializers import SearchWorksSerializer
from science.serializers import WorksSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


def query_type(content):
    if '*' in content or '?' in content:
        return 'wildcard'
    else:
        return 'fuzzy'


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_work(request, serializer):
    title = serializer.validated_data.get('title')
    author = serializer.validated_data.get('author')
    source = serializer.validated_data.get('source')
    start_year = serializer.validated_data.get('start_year')
    end_year = serializer.validated_data.get('end_year')

    es_query = WorkDocument.search()
    if title:
        es_query = es_query.query(query_type(title), title=title)
    if author:
        es_query = es_query.query('nested', path='authors', query=Q(query_type(author), authors__display_name=author))
    if source:
        es_query = es_query.query('nested', path='locations.source',
                                  query=Q(query_type(source), locations__source__display_name=source))
    if start_year and end_year:
        es_query = es_query.query('range', publication_date={'gte': f'{start_year}-01-01', 'lte': f'{end_year}-12-31'})

    es_results = es_query.execute()

    return api_response(ErrorCode.SUCCESS, data=es_results.to_dict())
