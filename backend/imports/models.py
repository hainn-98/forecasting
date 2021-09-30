from django.db import models
from safedelete.config import SOFT_DELETE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
import datetime

from clients.models import Client
from users.models import User
from .managers import ImportManager


class Import(SafeDeleteModel):
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

    _import = models.FloatField(null=True)
    domestic_economy = models.FloatField(null=True)
    foreign_invested_economy = models.FloatField(null=True)
    machinery_equipment = models.FloatField(null=True)
    plastic_material = models.FloatField(null=True)
    cashew = models.FloatField(null=True)
    rubber = models.FloatField(null=True)
    cloth =  models.FloatField(null=True)
    iron_steel = models.FloatField(null=True)
    animal_feed = models.FloatField(null=True)
    chemical = models.FloatField(null=True)
    textile_material = models.FloatField(null=True)
    metal = models.FloatField(null=True)
    corn = models.FloatField(null=True)
    chemical_product = models.FloatField(null=True)
    textile_yarn = models.FloatField(null=True)
    electronic_product = models.FloatField(null=True)
    cotton = models.FloatField(null=True)
    pesticide = models.FloatField(null=True)
    wood_product = models.FloatField(null=True)
    medicine = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='import_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='import_organizations',  on_delete=models.SET_NULL, unique=False, null=True)

    objects = ImportManager()

    class Meta():
        app_label = 'imports'
        db_table = 'import'