"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""
import math

from rest_framework.decorators import api_view

from science.request_serializers import SearchWorksSerializer, IdSerializer
from utils.decorators import validate_request
from MewScience.settings import ES
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_works(request, serializer):
    user = request.user
    if user.is_authenticated:
        print("yes")

    query = serializer.validated_data.get('query')
    page = serializer.validated_data.get('page')
    page_size = serializer.validated_data.get('page_size')
    min_score = serializer.validated_data.get('min_score')
    sort = serializer.validated_data.get('sort')
    order = serializer.validated_data.get('order')
    if page is None or page <= 0:
        page = 1
    if page_size is None or 25 < page_size <= 0:
        page_size = 10
    if min_score is None or min_score < 0:
        min_score = 10
    if sort is None:
        sort = "relevance"
    if order is None:
        order = "desc"

    query_body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "authorships.author.display_name", "abstract", "keywords.keyword",
                                   "concepts.display_name"]
                    }
                },
                "functions": [
                    {
                        "field_value_factor": {
                            "field": "cited_by_count",
                            "factor": 1.0,
                            "modifier": "log1p"
                        }
                    },
                    {
                        "script_score": {
                            "script": {
                                "source": "(doc['publication_date'].value.toEpochSecond() + 3790000000L) * params.factor",
                                "params": {
                                    "factor": 0.0000000002
                                }
                            }
                        }
                    }
                ],
                'score_mode': 'sum',  # 指定得分计算模式，这里是将所有函数的得分相加
                "boost_mode": "multiply"
            }
        },
        'from': (page - 1) * page_size,
        'size': page_size,
        "min_score": min_score,
    }
    if sort == "relevance":
        pass
    else:
        query_body["sort"] = [
            {
                sort: {
                    "order": order
                }
            }
        ]

    result = ES.search(index='works', body=query_body).get('hits')
    result['total']['page_num'] = math.ceil(result['total']['value'] / page_size)
    return api_response(ErrorCode.SUCCESS, data=result)


@api_view(['GET'])
@validate_request(IdSerializer)
def get_work(request, serializer):
    id = serializer.validated_data.get('id')
    result = ES.get(index='works', id=id)
    return api_response(ErrorCode.SUCCESS, result['_source'])
