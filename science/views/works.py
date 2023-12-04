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


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_work(request, serializer):
    title = serializer.validated_data.get('title')
    author = serializer.validated_data.get('author')
    # language = serializer.validated_data.get('language')

    es_query = WorkDocument.search()
    if title:
        es_query = es_query.query('match', title=title)
    if author:
        es_query = es_query.query('nested', path='authors', query=Q('match', authors__display_name=author))

    # results = es_query.to_queryset().all()
    es_results = es_query.execute()

    return api_response(ErrorCode.SUCCESS, data=es_results.to_dict())
