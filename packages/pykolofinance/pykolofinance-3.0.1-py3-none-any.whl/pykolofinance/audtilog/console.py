import datetime
import json
import logging

from django.urls import Resolver404, resolve

# Get the logger instance
logger = logging.getLogger(__name__)

class RequestResponseLoggerMiddleware:
    """
    Middleware to log requests and responses to the console.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        start_time = datetime.datetime.now()

        # Process the request
        response = self.get_response(request)

        # Log response details
        duration = datetime.datetime.now() - start_time
        try:
            resolver_match = resolve(request.path_info)
            url_name = resolver_match.url_name
            namespace = resolver_match.namespace
        except Resolver404:
            resolver_match = None
            url_name = None
            namespace = None

        request_data = {}
        if request.content_type == "application/json":
            try:
                request_data = json.loads(request.body)
            except json.JSONDecodeError:
                request_data = request.body.decode('utf-8')
        elif request.content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
            request_data = request.POST.dict()
            if request.FILES:
                request_data['files'] = {key: file.name for key, file in request.FILES.items()}

        if namespace != 'admin' and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logger.info({
                'request': {'path': request.path, 'method': request.method, },
                'body': request_data,
                'status_code': response.status_code,
                'duration': duration.total_seconds(),
                'response': json.loads(response.content.decode('utf-8')) if response.content else None
            })
        return response
