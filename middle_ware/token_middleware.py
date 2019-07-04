from django.utils.deprecation import MiddlewareMixin
from glaucus.settings import TOKEN_EXCLUDE_URL
from tools.redis_service import RedisService
from django.http import JsonResponse
import re
import logging

logger = logging.getLogger(__file__)

exclude_path = [re.compile(item) for item in TOKEN_EXCLUDE_URL]

class TokenMiddleware(MiddlewareMixin):
    """处理所有请求必须携带token才能通过认证"""
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 检测每个注册在settings中的url
        for each_url in exclude_path:
            if re.match(each_url, request.path):
                return callback(request, *callback_args, **callback_kwargs)

        token = request.META.get("HTTP_TOKEN")
        if not token or not RedisService.get_key(token):
            return JsonResponse({'code': 300002, 'msg': 'authorization failed', 'data': None})

        return callback(request, *callback_args, **callback_kwargs)
