from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def custom_drf_exception_handler(exc, context):
    # Update detail for validation exceptions
    if isinstance(exc, ValidationError):
        if 'non_field_errors' in exc.detail:
            exc.detail = exc.detail['non_field_errors']
    response = exception_handler(exc, context)
    if response:
        return response
    else:
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)