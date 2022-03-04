from rest_framework import status
from rest_framework.exceptions import APIException


class CustomUnauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid Token"
