from django.db import models
from rest_framework.serializers import ModelSerializer
from safedelete.config import SOFT_DELETE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from clients.models import Client
from users.models import User
from .managers import UnemploymentManager
import datetime 


class Unemployment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    MONTH_CHOICES = []
    for i in range(1, 13):
        MONTH_CHOICES.append((i, i))

    year = models.IntegerField(choices=YEAR_CHOICES, 
           default=datetime.datetime.now().year)
    month = models.SmallIntegerField(choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    rate = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='unemployment_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='unemployment_organizations',  on_delete=models.SET_NULL, unique=False, null=True)

    objects = UnemploymentManager()

    class Meta():
        app_label = 'unemployments'
        db_table = 'unemployment'