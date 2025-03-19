# -*- coding: utf-8 -*-
# @Author: Richard
# @File: utils.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response
    response = exception_handler(exc, context)

    # Custom handling for UnsupportedMediaType errors
    if response is not None and response.status_code == 415:
        try:
            # Try to handle the request anyway by parsing the raw data
            request = context['request']
            view = context['view']
            return view.post(request)
        except:
            pass

    return response