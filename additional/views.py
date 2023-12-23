from rest_framework.decorators import api_view
from additional.models import Project, ProjectOutputSerializer, Patent, PatentOutputSerializer, RewardOutputSerializer, \
    Reward
from additional.request_serializers import ProjectSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['POST'])
@validate_request(ProjectSerializer)
def get_project(request, serializer):
    id = serializer.validated_data.get('author_id')
    project_list = Project.objects.filter(authors__contains=[int(id)]).all()
    data = ProjectOutputSerializer(project_list, many=True).data
    return api_response(ErrorCode.SUCCESS, data=data)


@api_view(['POST'])
@validate_request(ProjectSerializer)
def get_patent(request, serializer):
    id = serializer.validated_data.get('author_id')
    patent_list = Patent.objects.filter(authors_r__contains=[int(id)]).all()
    data = PatentOutputSerializer(patent_list, many=True).data
    return api_response(ErrorCode.SUCCESS, data=data)


@api_view(['POST'])
@validate_request(ProjectSerializer)
def get_reward(request, serializer):
    id = serializer.validated_data.get('author_id')
    reward_list = Reward.objects.filter(authors_r__contains=[int(id)]).all()
    data = RewardOutputSerializer(reward_list, many=True).data
    return api_response(ErrorCode.SUCCESS, data=data)