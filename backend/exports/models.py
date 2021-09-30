from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
import datetime

from clients.models import Client
from users.models import User
from .managers import ExportManager


class Export(SafeDeleteModel):
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

    export = models.FloatField(null=True)
    domestic_economy = models.FloatField(null=True)
    foreign_invested_economy = models.FloatField(null=True)
    footwear = models.FloatField(null=True)
    textile_product = models.FloatField(null=True)
    textile_yarn = models.FloatField(null=True)
    wood_product = models.FloatField(null=True)
    machinery_equipment = models.FloatField(null=True)
    transport_vehicle = models.FloatField(null=True)
    coffe = models.FloatField(null=True)
    iron_steel_product = models.FloatField(null=True)
    electronic_product = models.FloatField(null=True)
    cashew = models.FloatField(null=True)
    plastic_product = models.FloatField(null=True)
    pepper = models.FloatField(null=True)
    rubber = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='export_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='export_organizations',  on_delete=models.SET_NULL, unique=False, null=True)

    objects = ExportManager()

    class Meta():
        app_label = 'exports'
        db_table = 'export'