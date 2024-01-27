from django.http import JsonResponse
from django.shortcuts import render
from category.exception import CategoryDeleteFailed,RootCategoryDeleteFailed,CategoryWithResource
from django.core.exceptions import ObjectDoesNotExist
import traceback

class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        traceback.print_exc()
        if isinstance(exception, RootCategoryDeleteFailed) or isinstance(exception, CategoryDeleteFailed) or isinstance(exception,ObjectDoesNotExist) or isinstance(exception,CategoryWithResource):
            return JsonResponse({'error': str(exception)}, status=500)
        # 处理异常逻辑
        error_message = str(exception)
        return render(request, 'error/error.html', {"error_message": error_message})
