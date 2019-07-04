from .json_response import JsonResponse
from django.db import DatabaseError
from rest_framework.views import exception_handler
from .base import APIExceptionFactory

import logging

logger = logging.getLogger(__file__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    logger.error(f'exc = {exc}, response = {response}')

    response = APIExceptionFactory.get_exception(exc)
    if response:
        response = JsonResponse(data=None, msg=response.default_detail, code=response.default_code,
                                status=response.status_code)

    return response
