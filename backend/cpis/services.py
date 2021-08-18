from .models import Cpi
from utils.custom_exceptions import *


def get_cpi_by(raise_exception=True, **kwargs):
    cpi = Cpi.objects.filter(**kwargs).all()
    if not cpi and raise_exception: 
        raise ObjectNotFound
    return cpi

def add_cpi(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    cpi = get_cpi_by(raise_exception=False, year=data['year'], month = data['month']).first()
    if cpi:
        raise DuplicateEntry(entry=str(cpi.year) + str(cpi.month), key='year and month')
    cpi = Cpi.objects.create(**dict(data))
    return cpi

def update_cpi(cpi, data):
    if not any(data.values()):
        raise ValidationError
    cpi.CPI = data.get('CPI') or cpi.CPI
    cpi.food_service = data.get('food_service') or cpi.food_service
    cpi.eating_out = data.get('eating_out') or cpi.eating_out
    cpi.cereal = data.get('cereal') or cpi.cereal
    cpi.food = data.get('food') or cpi.food
    cpi.beverage_cigarette = data.get('beverage_cigarette') or cpi.beverage_cigarette
    cpi.garment = data.get('garment') or cpi.garment
    cpi.household_equipment = data.get('household_equipment') or cpi.household_equipment
    cpi.housing = data.get('housing') or cpi.housing
    cpi.medicine_medical_service = data.get('medicine_mediacl_service') or cpi.medicine_medical_service
    cpi.communication = data.get('communication') or cpi.communication
    cpi.telecomunication = data.get('telecommunication') or cpi.telecommunication
    cpi.education = data.get('education') or cpi.education
    cpi.culture_entertainment_travel = data.get('culture_entertainment_travel') or cpi.culture_entertainment_travel
    cpi.other_good_services = data.get('other_good_services') or cpi.other_good_services
    cpi.base_period = data.get('base_period') or cpi.base_period
    cpi.save(update_fields=['CPI', 'food_service', 'eating_out', 'cereal', 'food', 'beverage_cigarette', 'garment', 
                            'household_equipment', 'housing', 'medicine_medical_service', 'communication', 'telecommunication', 
                            'education', 'culture_entertainment_travel', 'other_good_services', 'base_period'])
    return cpi

def delete_cpi(cpi):
    cpi.delete()
    return cpi
