from django.db import models
from safedelete.config import SOFT_DELETE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from clients.models import Client
from users.models import User
from .managers import RevenueExpenditureManager
import datetime


class RevenueExpenditure(SafeDeleteModel):
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
    revenue = models.FloatField(null=True)
    expenditure = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='rev_exp_creators', on_delete=models.SET_NULL, unique=False, null=True)
    organization = models.ForeignKey(Client, related_name='rev_exp_organizations',  on_delete=models.SET_NULL, unique=False, null=True)

    objects = RevenueExpenditureManager()

    class Meta():
        app_label = 'revenue_expenditures'
        db_table = 'revenue_expenditure'