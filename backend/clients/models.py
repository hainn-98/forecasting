from http import client
from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from .managers import ClientManager


class Client(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    client_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClientManager()

    class Meta:
        app_label = 'clients'
        db_table = 'client'

    def __str__(self):
        return self.client_name
