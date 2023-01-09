import os

from django.contrib.auth.models import User
from django.db import transaction

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from typing import Tuple


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }
    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:

    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True


def user_get_me(*, user: User):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'name': user.first_name + user.last_name,
    }



def validate_google_auth_token_and_get_data(google_auth_token):
    # client_id = 'YOUR_GOOGLE_CLIENT_ID'
    client_id = '179339673846-nipkr8ip8jnlbd3gtlmvd7i6eqhn5k3t.apps.googleusercontent.com'
    request = google_requests.Request()
    user_info = id_token.verify_oauth2_token(google_auth_token, request, client_id)
    return user_info