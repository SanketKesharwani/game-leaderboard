from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from typing import Callable, Any

def handle_api_exceptions(view_method: Callable) -> Callable:
    """
    Decorator for DRF API view methods to provide consistent exception handling.
    Catches ValidationError, ValueError, and generic Exception, returning
    a standardized JSON response with appropriate status codes.
    """
    @wraps(view_method)
    def _wrapped_view(self, request, *args, **kwargs) -> Response:
        try:
            return view_method(self, request, *args, **kwargs)
        except ValidationError as validation_error:
            return Response(
                data={
                    "error": "Validation error",
                    "details": str(validation_error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as value_error:
            return Response(
                data={
                    "error": "Value error",
                    "details": str(value_error)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as unexpected_error:
            return Response(
                data={
                    "error": "Internal server error",
                    "details": str(unexpected_error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return _wrapped_view 