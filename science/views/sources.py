"""
============================
# @Time    : 2023/12/23 16:41
# @Author  : Elaikona
# @FileName: sources.py
===========================
"""
from rest_framework.decorators import api_view

from MewScience.settings import ES
from science.request_serializers import GetHotSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(GetHotSerializer)
def get_hot(request, serializer):
    index = serializer.validated_data.get('index')
    sort = serializer.validated_data.get('sort')

    if index not in ['institutions', 'concepts', 'authors', 'sources']:
        return api_response(ErrorCode.INVALID_DATA)

    query_body = {
        "query": {
            "match_all": {}
        },
        "size": 50
    }
    if sort not in ['h_index', '2yr_mean_citedness', 'i10_index']:
        sort = 'h_index'
    else:
        query_body["sort"] = [
            {
                "summary_stats." + sort: {
                    "order": "desc"
                }
            }
        ]
    result = ES.search(index=index, body=query_body).get('hits')
    return api_response(ErrorCode.SUCCESS, result)
