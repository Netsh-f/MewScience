"""
============================
# @Time    : 2023/12/20 21:37
# @Author  : Elaikona
# @FileName: authors.py
===========================
"""

from rest_framework.decorators import api_view

from MewScience.settings import ES
from science.request_serializers import SearchAuthorsSerializer, IdSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(SearchAuthorsSerializer)
def search_authors(request, serializer):
    name = serializer.validated_data.get('name')
    institution = serializer.validated_data.get('institution')
    page = serializer.validated_data.get('page')
    page_size = serializer.validated_data.get('page_size')
    if institution is None:
        institution = ""
    if page is None or page <= 0:
        page = 1
    if page_size is None or 25 < page_size <= 0:
        page_size = 10

    query_body = {
        'query': {
            'bool': {
                'should': [
                    {'match': {'display_name': name}},
                    {'match': {'last_known_institution.display_name': institution}},
                ],
                'minimum_should_match': 1,
            }
        },
        'from': (page - 1) * page_size,
        'size': page_size
    }
    result = ES.search(index='authors', body=query_body)
    return api_response(ErrorCode.SUCCESS, data=result.get('hits'))


@api_view(['GET'])
@validate_request(IdSerializer)
def get_researcher(request, serializer):
    id = serializer.validated_data.get('id')
    result = ES.get(index='authors', id=id)
    return api_response(ErrorCode.SUCCESS, result['_source'])
