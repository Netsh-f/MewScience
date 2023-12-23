"""
============================
# @Time    : 2023/12/20 21:37
# @Author  : Elaikona
# @FileName: authors.py
===========================
"""
import math

from rest_framework.decorators import api_view

from MewScience.settings import ES
from portal.views import get_user_by_portal
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
    min_score = serializer.validated_data.get('min_score')
    if page is None or page <= 0:
        page = 1
    if page_size is None or 25 < page_size <= 0:
        page_size = 10
    if min_score is None or min_score < 0:
        min_score = 10

    query_body = {
        'query': {
            'bool': {
                'should': [
                    {'match': {'display_name': {'query': name, 'boost': 1.3}}},
                ],
                'minimum_should_match': 1,
            }
        },
        'from': (page - 1) * page_size,
        'size': page_size,
        "min_score": min_score,
    }
    if institution is not None:
        query_body['query']['bool']['should'].append({'match': {'last_known_institution.display_name': institution}})
    result = ES.search(index='authors', body=query_body).get('hits')
    result['total']['page_num'] = math.ceil(result['total']['value'] / page_size)
    return api_response(ErrorCode.SUCCESS, data=result)


@api_view(['GET'])
@validate_request(IdSerializer)
def get_researcher(request, serializer):
    id = serializer.validated_data.get('id')
    result = ES.get(index='authors', id=id)
    user_dict = get_user_by_portal(id)
    result['_source'].update(user_dict)
    return api_response(ErrorCode.SUCCESS, result['_source'])
