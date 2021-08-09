from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import AuthToken
from utils.custom_exceptions import *


def expire_token(user):
    try:
        for auth_token in user.auth_tokens.all():
            auth_token.expired_at = timezone.now()
            auth_token.user_id = None
            auth_token.save(update_fields=['expired_at', 'user_id'])
            auth_token.delete()
    except AuthToken.DoesNotExist:
        pass


def get_auth_token_by(raise_exception=True, only_deleted=False, **kwargs):
    key = kwargs.get('key')
    if only_deleted:
        auth_token = AuthToken.objects.deleted_only().filter(**kwargs).first()
    else:
        auth_token = AuthToken.objects.filter(key=key).first()
    if not auth_token and raise_exception:
        raise ObjectNotFound
    return auth_token


def create_token(user):
    auth_token = AuthToken.objects.create(user=user)
    return auth_token


def token_expire_handler(auth_token):
    if auth_token.is_expired:
        auth_token = create_token(user=auth_token.user)
    return auth_token.is_expired, auth_token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            auth_token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed
        is_expired, auth_token = token_expire_handler(auth_token)

        if is_expired:
            raise AuthenticationFailed
        return auth_token.user, auth_token
