#-*- encoding:utf-8 -*-

import sys
from django.views.debug import technical_500_response

class AdminSeeErrorMiddleWare(object):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
