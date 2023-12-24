"""
============================
# @Time    : 2023/12/23 16:41
# @Author  : Elaikona
# @FileName: sources.py
===========================
"""
import copy

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

    if index not in ['institutions', 'concepts', 'authors', 'sources']:
        return api_response(ErrorCode.INVALID_DATA)

    query_body = {
        "query": {
            "match_all": {}
        },
        "size": 10
    }
    query_body_h_index = copy.deepcopy(query_body)
    query_body_2yr_mean_citedness = copy.deepcopy(query_body)
    query_body_i10_index = copy.deepcopy(query_body)
    query_body_h_index["sort"] = [
        {
            "summary_stats.h_index": {
                "order": "desc"
            }
        }
    ]
    query_body_2yr_mean_citedness["sort"] = [
        {
            "summary_stats.2yr_mean_citedness": {
                "order": "desc"
            }
        }
    ]
    query_body_i10_index["sort"] = [
        {
            "summary_stats.i10_index": {
                "order": "desc"
            }
        }
    ]
    result_h_index = ES.search(index=index, body=query_body_h_index).get('hits').get('hits')
    result_2yr_mean_citedness = ES.search(index=index, body=query_body_2yr_mean_citedness).get('hits').get('hits')
    result_2yr_i10_index = ES.search(index=index, body=query_body_i10_index).get('hits').get('hits')
    merged_list = result_h_index + result_2yr_mean_citedness + result_2yr_i10_index
    unique_set = {item["_id"]: item for item in merged_list}.values()
    result_list = list(unique_set)
    return api_response(ErrorCode.SUCCESS, result_list)
