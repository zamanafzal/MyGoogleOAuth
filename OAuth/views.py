from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from OAuth.utils import validate_google_auth_token_and_get_data, user_get_or_create, user_get_me


class UserGoogleAuthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs) -> Response:
        """
        Google User sign up/in API.
        :param request:
        :return:
        """
        google_auth_token = request.data['headers'].get('Authorization')
        user_info = validate_google_auth_token_and_get_data(google_auth_token)

        user_data = {
            'email': user_info.get('email'),
            'username': user_info.get('email'),
            'first_name': user_info.get('given_name'),
            'last_name': user_info.get('family_name'),
        }
        user, _ = user_get_or_create(**user_data)
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': user_get_me(user=user)}
        return Response(data=data)
