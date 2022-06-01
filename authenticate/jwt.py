from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from .models import User

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split()

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Token is not valid.")

        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            email = payload['email']
            user = User.objects.get(email=email)

            return (user, token)

        except jwt.ExpiredSignatureError as expired:
            raise exceptions.AuthenticationFailed("Token is expired.")
        except jwt.DecodeError as invalid:
            raise exceptions.AuthenticationFailed("Token is not valid.")
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed("User does not exists.")

        return super().authenticate(request)