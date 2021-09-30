import binascii
from datetime import timedelta
import os

from django.utils import timezone
from django.conf import settings

from auth_tokens.services import expire_token, create_token
from utils.email_sending import send_init_pwd, send_reset_pwd_token
from .models import User
from utils.custom_exceptions import *


def get_user_by(raise_exception=True, with_deleted=False, **kwargs):
    if with_deleted:
        user = User.objects.all_with_deleted().filter(**kwargs).first()
    else:
        user = User.objects.filter(**kwargs).first()
    if not user and raise_exception:
        raise Unauthenticated
    return user    

def create_user(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    user = get_user_by(email=data['email'], raise_exception=False, with_deleted=True)
    if user:
        raise DuplicateEntry(entry=user.email, key='email')
    init_password = binascii.hexlify(os.urandom(10)).decode()
    data['password'] = init_password
    user = User.objects.create_user(**dict(data))
    send_init_pwd(user=user, password=init_password)
    return user, init_password

def update_user(user, data):
    if not any(data.values()):
        raise ValidationError
    user.name = data.get('name') or user.name
    user.save(update_fields=['name'])
    return user

def deactivate_user(user):
    expire_token(user=user)
    user.is_active = False
    user.save(update_fields=['is_active'])
    user.delete()
    return user

def activate(user):
    user.undelete()
    user.is_active = True
    user.save(update_fields=['is_active'])
    return user   

def change_password(user, data):
    if data.get('password') != data.get('password_confirmation'):
        raise ValidationError('Password and password confirmation do not match')
    if not user.check_password(raw_password=data.get('old_password')):
        raise Unauthenticated
    user.set_password(data.get('password'))
    user.change_init_password = True
    user.is_active = True
    user.save(update_fields=['password', 'change_init_password', 'is_active'])
    return user

def generate_password_token(data):
    email = data.get('email')
    user = get_user_by(email=email)
    user.reset_password_token = binascii.hexlify(os.urandom(20)).decode()
    user.reset_password_token_expired_at = timezone.now() + timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
    send_reset_pwd_token(user=user)
    user.save(update_fields=['reset_password_token', 'reset_password_token_expired_at'])
    return user

def reset_password(data):
    if data.get('password') != data.get('password_confirmation'):
        raise ValidationError
    user = get_user_by(reset_password_token=data.get('reset_password_token'))
    if not user:
        raise InvalidToken
    elif user.reset_password_token_expired_at < timezone.now():
        raise TokenExpired
    user.set_password(data.get('password'))
    user.change_init_password = True
    user.is_active = True
    user.save(update_fields=['password', 'change_init_password', 'is_active'])
    return user

def authenticate_user(email, password):
    user = get_user_by(email=email)
    if not user.check_password(raw_password=password):
        raise Unauthenticated
    auth_token = create_token(user=user)
    return auth_token