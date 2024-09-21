from rest_framework.renderers import JSONRenderer
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse


class MyExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0]
        if (error_response.type == "validation_error"
                and error.attr != "non_field_errors"
                and error.attr is not None
                and error.detail[:4] == 'This'):
            error_message = error.detail.replace('This', error.attr)
        else:
            error_message = error.detail
        return {
            "success": False,
            "error": {
                "message": error_message
            }
        }
