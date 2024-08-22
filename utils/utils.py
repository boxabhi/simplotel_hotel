from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "status": False,
            "message": "An error occurred",
            "data": response.data
        }, status=response.status_code)

    return Response({
        "status": False,
        "message": "Something went wrong",
        "data": {}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
