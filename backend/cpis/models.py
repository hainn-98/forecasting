from clients.models import Client
from django.db import models

from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from .managers import CpiManager
from users.models import User
import datetime


class Cpi(SafeDeleteModel):
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

    CPI = models.FloatField(null=True)
    food_service = models.FloatField(null=True)
    eating_out = models.FloatField(null=True)
    cereal = models.FloatField(null=True)
    food = models.FloatField(null=True)
    beverage_cigarette = models.FloatField(null=True)
    garment = models.FloatField(null=True)
    household_equipment = models.FloatField(null=True)
    housing = models.FloatField(null=True)
    medicine_medical_service = models.FloatField(null=True)
    communication = models.FloatField(null=True)
    telecommunication = models.FloatField(null=True)
    education = models.FloatField(null=True)
    culture_entertainment_travel = models.FloatField(null=True)
    other_good_services = models.FloatField(null=True)
    base_period = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='cpi_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='cpi_organizations',  on_delete=models.SET_NULL, unique=False, null=True)
    
    objects = CpiManager()

    class Meta():
        app_label = 'cpis'
        db_table = 'cpi' 