# -*- coding: utf-8 -*-
# @Author: Richard
# @File: middleware.py
import json

class JsonParsingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json' or request.path in ['/signup/', '/signin/']:
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    if hasattr(request, '_body'):
                        data = json.loads(request._body.decode('utf-8'))
                        setattr(request, '_json_body', data)
                except:
                    pass

        response = self.get_response(request)
        return response