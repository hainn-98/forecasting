from django.db import models
from safedelete.config import SOFT_DELETE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from clients.models import Client
from users.models import User
from .managers import IipManager
import datetime


class Iip(SafeDeleteModel):
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

    IIP = models.FloatField(null=True)
    mining_industry = models.FloatField(null=True)
    manufacturing_processing_industry = models.FloatField(null=True)
    gas_electricity_industry = models.FloatField(null=True)
    waste_treatment_water_supply = models.FloatField(null=True)
    mineral_exploitation = models.FloatField(null=True)
    food = models.FloatField(null=True)
    cigarette = models.FloatField(null=True)
    textile = models.FloatField(null=True)
    costume = models.FloatField(null=True)
    leather_product = models.FloatField(null=True)
    paper_product = models.FloatField(null=True)
    chemical_product = models.FloatField(null=True)
    plastic_product = models.FloatField(null=True)
    non_metalic_mineral_product = models.FloatField(null=True)
    prefabricated_metal_product = models.FloatField(null=True)
    electrical_product = models.FloatField(null=True)
    motor_vehicle = models.FloatField(null=True)
    furniture = models.FloatField(null=True)
    other_manufacturing_processing = models.FloatField(null=True)
    water_supply = models.FloatField(null=True)
    gas_electricity = models.FloatField(null=True)
    other_products = models.FloatField(null=True)
    base_period = models.CharField(max_length=50 ,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='iip_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='iip_organizations',  on_delete=models.SET_NULL, unique=False, null=True)

    objects = IipManager()

    class Meta():
        app_label = 'iips'
        db_table = 'iip'