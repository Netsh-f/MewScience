"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""
from rest_framework.decorators import api_view

from science.request_serializers import SearchWorksSerializer
from utils.decorators import validate_request
from MewScience.settings import ES
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_works(request, serializer):
    query = serializer.validated_data.get('query')
    page = serializer.validated_data.get('page')
    page_size = serializer.validated_data.get('page_size')
    if page is None or page <= 0:
        page = 1
    if page_size is None or 25 < page_size <= 0:
        page_size = 10

    query_body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "authorships.author.display_name","abstract", "keywords.keyword",
                                   "concepts.display_name"]
                    }
                },
                "functions": [

                    {
                        "script_score": {
                            "script": {
                                "source": "doc['publication_date'].date.millis * params.factor",
                                "params": {
                                    "factor": 0.0000001
                                }
                            }
                        }
                    }
                ],
                "boost_mode": "multiply"
            }
        },
        "min_score": 10.0,
    }

    result = ES.search(index='works', body=query_body)
    return api_response(ErrorCode.SUCCESS, data=result.get('hits'))
