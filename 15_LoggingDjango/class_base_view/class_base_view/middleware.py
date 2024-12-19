import logging
import time

application_logger = logging.getLogger('application-logger')
error_logger = logging.getLogger('error-logger')
performance_logger = logging.getLogger('performance-logger')

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        application_logger.info(request.get_full_path())
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        error_logger.error(exception, exc_info=True)

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        response_time = end_time - start_time
        
        performance_logger.info(f'{request.method} {request.get_full_path()}: {response_time}s')
        return response
