"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""
import math

from elastic_transport import ConnectionTimeout
from elasticsearch.exceptions import NotFoundError
from requests import JSONDecodeError
from rest_framework.decorators import api_view

from science.request_serializers import SearchWorksSerializer, IdSerializer, AdvancedSearchWorksSerializer
from science.utils.openalex import get_work_from_openalex
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
    if sort not in ["publication_date", "cited_by_count"]:
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


def get_field_name(name):
    if name in ['title', 'publication_date']:
        return name
    elif name == 'author':
        return 'authorships.author.display_name'
    elif name == 'source':
        return 'locations.source.display_name'
    elif name == 'concept':
        return 'concepts.display_name.keyword'


@api_view(['POST'])
@validate_request(AdvancedSearchWorksSerializer)
def advanced_search_works(request, serializer):
    condition_list = serializer.validated_data.get('query')
    page = serializer.validated_data.get('page')
    page_size = serializer.validated_data.get('page_size')
    min_score = serializer.validated_data.get('min_score')
    sort = serializer.validated_data.get('sort')
    order = serializer.validated_data.get('order')
    aggs_size = serializer.validated_data.get('aggs_size')

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
    if aggs_size is None:
        aggs_size = 10

    query_body = {
        "query": {
            "bool": {
                "must": [],
                "should": [],
                "must_not": []
            }
        },
        'from': (page - 1) * page_size,
        'size': page_size,
        "min_score": min_score,
        "aggs": {
            "concept": {
                "terms": {
                    "field": "concepts.display_name.keyword",  # 请注意，这里使用了 ".keyword" 表示确保不会进行分词
                    "size": aggs_size  # 可以根据实际需求设置返回的桶的数量
                }
            },
            "country": {
                "terms": {
                    "field": "authorships.institutions.country_code.keyword",
                    "size": aggs_size
                }
            },
            "source": {
                "terms": {
                    "field": "locations.source.display_name.keyword",
                    "size": aggs_size
                }
            },
            "keyword": {
                "terms": {
                    "field": "keywords.keyword.keyword",
                    "size": aggs_size
                }
            },
            "language": {
                "terms": {
                    "field": "language.keyword",
                    "size": aggs_size
                }
            },
            "mesh": {
                "terms": {
                    "field": "mesh.descriptor_name.keyword",
                    "size": aggs_size
                }
            },
        },
    }

    multi_search_function_score = {
        "query": {
            "multi_match": {
                "query": "",
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

    for condition in condition_list:
        if condition['field'] == 'publication_date':
            start_year, end_year = condition['query'].split('-')
            start_date = f"{start_year}-01-01"
            end_date = f"{end_year}-12-31"
            query_body['query']['bool'][condition['logic']].append({
                'range': {
                    get_field_name(condition['field']): {
                        'gte': start_date,
                        'lte': end_date
                    }
                }
            })
        elif condition['field'] == 'concept':
            query_body['query']['bool'][condition['logic']].append({
                'term': {
                    get_field_name(condition['field']): condition['query']
                }
            })
        elif condition['field'] == 'multi_search':
            multi_search_function_score['query']['multi_match']['query'] = condition['query']
            query_body['query']['bool'][condition['logic']].append({
                'function_score': multi_search_function_score
            })
        else:
            query_body['query']['bool'][condition['logic']].append({
                'match': {
                    get_field_name(condition['field']): condition['query']
                }
            })

    if sort not in ["publication_date", "cited_by_count"]:
        pass
    else:
        query_body["sort"] = [
            {
                sort: {
                    "order": order
                }
            }
        ]
    result = ES.search(index='works', body=query_body)
    result['hits']['total']['page_num'] = math.ceil(result['hits']['total']['value'] / page_size)
    return api_response(ErrorCode.SUCCESS, result)


def get_work_from_es_or_openalex(id):
    work = None
    try:
        work = ES.get(index='works', id=id)['_source']
    except NotFoundError:
        work = get_work_from_openalex(id)
    return work


@api_view(['GET'])
@validate_request(IdSerializer)
def get_work(request, serializer):
    id = serializer.validated_data.get('id')
    result = None
    try:
        result = get_work_from_es_or_openalex(id)
    except JSONDecodeError:
        return api_response(ErrorCode.WORK_NOT_FOUND)

    if request.user.is_authenticated and str(id) in request.user.userprofile.collect_list:
        result['collected'] = True
    else:
        result['collected'] = False
    return api_response(ErrorCode.SUCCESS, result)
