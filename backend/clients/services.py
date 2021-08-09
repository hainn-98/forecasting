from .models import Client
from users.services import create_user, deactivate_user, get_user_by
from utils.custom_exceptions import *


def create_client(data):
    validated_data = data.copy()
    user = get_user_by(email=data.get('email'), raise_exception=False)
    if user:
        raise DuplicateEntry(entry=user.email, key='email')
    client_name = validated_data.get('client_name')
    client = get_client_by(client_name=client_name, raise_exception=False)
    if client:
        raise DuplicateEntry(entry=client_name, key='client_name')
    client = Client.objects.create(client_name=client_name, address=validated_data.get('address'))
    validated_data.pop('client_name')
    validated_data.pop('address')
    validated_data['client_id'] = client.id
    create_user(data=validated_data, role=2)
    return client


def get_client_by(raise_exception=True, only_deleted=False, **kwargs):
    if only_deleted:
        client = Client.objects.deleted_only().filter(**kwargs).first()
    else:
        client = Client.objects.filter(**kwargs).first()
    if not client and raise_exception:
        raise ObjectNotFound
    return client


def update_client(client, data):
    if not any(data.values()):
        raise ValidationError
    client.client_name = data.get('client_name')
    client.save(update_fields=['client_name'])
    return client


def deactivate_client(client):
    for user in client.users.all():
        deactivate_user(user=user)
    client.is_active = False
    client.save(update_fields=['is_active'])
    client.delete()
    return client


def activate_client(client):
    client.is_active = True
    client.save(update_fields=['is_active'])
    return client