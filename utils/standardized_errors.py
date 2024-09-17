from rest_framework.renderers import JSONRenderer
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse


class MyExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0]
        return {
            "success": False,
            "error": {
                "message": error.detail
            }
        }
