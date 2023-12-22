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

    # query_body = {
    #     'query': {
    #         'multi_match': {
    #             'query': query,
    #             'fields': ['title^3', 'authorships.author.display_name^4', 'abstract^2', 'keywords.keyword^2',
    #                        'concepts.display_name']
    #         }
    #     },
    #     'from': (page - 1) * page_size,
    #     'size': page_size
    # }
    query_body = {
        'query': {
            'function_score': {
                'query': {
                    'multi_match': {
                        'query': 'your_search_query',
                        'fields': ['title', 'abstract', 'keywords', 'concepts', 'locations']
                    }
                },
                'functions': [
                    {
                        'field_value_factor': {
                            'field': 'cited_by',
                            'factor': 1.5,  # 调整因子，根据实际需求设置
                            'modifier': 'log1p'  # 可选的修饰符，根据实际需求设置
                        }
                    }
                    # 可以添加其他函数来调整得分，如果需要的话
                ],
                'score_mode': 'sum',  # 指定得分计算模式，这里是将所有函数的得分相加
                'boost_mode': 'replace'  # 指定权重的计算方式，这里是替换原始得分
            }
        },
        'from': (page - 1) * page_size,
        'size': page_size
    }
    result = ES.search(index='works', body=query_body)
    return api_response(ErrorCode.SUCCESS, data=result.get('hits'))
