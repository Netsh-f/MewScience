"""
============================
# @Time    : 2023/12/20 21:37
# @Author  : Elaikona
# @FileName: authors.py
===========================
"""
import json
import math

from rest_framework.decorators import api_view

from MewScience.settings import ES
from additional.models import Patent, PatentOutputSerializer, Reward, RewardOutputSerializer, Project, \
    ProjectOutputSerializer
from data.utils.regex_utils import get_id
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
    result = ES.get(index='authors', id=id).get('_source')
    user_dict = get_user_by_portal(id)
    result.update(user_dict)

    patents = Patent.objects.filter(authors_r__contains=id).all()
    result['patents'] = PatentOutputSerializer(patents, many=True).data
    rewards = Reward.objects.filter(authors_r__contains=id).all()
    result['rewards'] = RewardOutputSerializer(rewards, many=True).data
    projects = Project.objects.filter(authors_r__contains=id).all()
    result['projects'] = ProjectOutputSerializer(projects, many=True).data

    if request.user.is_authenticated and str(id) in request.user.userprofile.follow_list:
        result['followed'] = True
    else:
        result['followed'] = False

    return api_response(ErrorCode.SUCCESS, result)


@api_view(['GET'])
@validate_request(IdSerializer)
def get_related_researcher(request, serializer):
    id = serializer.validated_data.get('id')
    # query_body = {
    #     "query": {
    #         "match": {
    #             "authorships.author.id": {
    #                 "query": "https://openalex.org/A" + str(id)
    #             }
    #         }
    #     },
    #     "min_score": 10,
    #     "size": 50,
    # }
    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"authorships.author.id": f"{id}"}}
                ]
            }
        },
        "size": 50
    }

    works = ES.search(index='works', body=query_body).get('hits').get('hits')
    researchers_result = {}
    institutions_result = {}
    for work in works:
        for author_info in work.get('_source').get('authorships'):
            author_institutions = author_info.get('institutions')
            author = author_info.get('author')
            for institution in author_institutions:
                institution_id = get_id(institution.get('id'))
                if institution_id not in institutions_result:
                    institutions_result[institution_id] = institution
                    institutions_result[institution_id]['times'] = 1
                else:
                    institutions_result[institution_id]['times'] += 1

            author_id = get_id(author.get('id'))
            if author_id not in researchers_result:
                researchers_result[author_id] = author
                researchers_result[author_id]['times'] = 1
            else:
                researchers_result[author_id]['times'] += 1
    return api_response(ErrorCode.SUCCESS,
                        {"works": works, "researchers": researchers_result, "institutions": institutions_result})
