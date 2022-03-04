from rest_framework.permissions import BasePermission

from api_token.exceptions import CustomUnauthorized


class HasValidApiToken(BasePermission):
    """
    Checks if the token provided with the api is valid and Active
    """

    def has_permission(self, request, view) -> bool:
        # token = request.parser_context['kwargs']['token']
        token: str = view.kwargs['token'].strip()

        # Check if token received in url is not empty
        if token:
            from .models import ApiToken
            try:
                # Fetch ApiToken object from database
                token_obj = ApiToken.objects.get(token=token)
                # Check if token is active
                if token_obj.is_active:
                    return True
                else:
                    raise CustomUnauthorized(detail="Token is not active.")
            except ApiToken.DoesNotExist:
                raise CustomUnauthorized(detail="Token is not valid.")
        else:
            # If token is empty return False
            raise CustomUnauthorized(detail="Token is not valid.")
