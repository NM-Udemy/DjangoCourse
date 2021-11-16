# middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin
import time

application_logger = logging.getLogger('application-logger')
error_logger = logging.getLogger('error-logger')
performance_logger = logging.getLogger('performance-logger')

class MyMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs): # viewを呼び出す前に実行
        application_logger.info(request.get_full_path())
        
    def process_exception(self, request, exception):
        error_logger.error(exception, exc_info=True)


class PerformanceMiddlware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        start_time = time.time()
        request.start_time = start_time

    def process_template_response(self, request, response):
        response_time = time.time() - request.start_time
        performance_logger.info(f'{request.get_full_path()}: {response_time}s')
        return response