from .models import Unemployment
from utils.custom_exceptions import *


def get_unemployment_by(raise_exception=True, **kwargs):
    unemployment = Unemployment.objects.filter(**kwargs).all()
    if not unemployment and raise_exception: 
        raise ObjectNotFound
    return unemployment

def add_unemployment(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    unemployment = get_unemployment_by(raise_exception=False, year=data['year'], month = data['month']).first()
    if unemployment:
        raise DuplicateEntry(entry=str(unemployment.year) + str(unemployment.month), key='year and month')
    unemployment = Unemployment.objects.create(**dict(data))
    return unemployment

def update_unemployment(unemployment, data):
    if not any(data.values()):
        raise ValidationError
    unemployment.rate = data.get('rate') or unemployment.rate
    unemployment.save(update_fields=['rate'])
    return unemployment

def delete_unemployment(unemployment):
    unemployment.delete()
    return unemployment
