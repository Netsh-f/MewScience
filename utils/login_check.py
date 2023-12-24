# ------- Litang Save The World! -------
#
# @Time    : 2023/12/24 13:45
# @Author  : Lynx
# @File    : login_check.py
#

from functools import wraps

from rest_framework.decorators import api_view

from utils.error_code import ErrorCode


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return api_view(ErrorCode.NOT_LOGGED_IN)
        return view_func(request, *args, **kwargs)
    return wrapper