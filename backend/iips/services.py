from .models import Iip
from utils.custom_exceptions import *


def get_iip_by(raise_exception=True, **kwargs):
    iip = Iip.objects.filter(**kwargs).all()
    if not iip and raise_exception: 
        raise ObjectNotFound
    return iip

def add_iip(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    iip = get_iip_by(raise_exception=False, year=data['year'], month = data['month']).first()
    if iip:
        raise DuplicateEntry(entry=str(iip.year) + str(iip.month), key='year and month')
    iip = Iip.objects.create(**dict(data))
    return iip

def update_iip(iip, data):
    if not any(data.values()):
        raise ValidationError
    iip.IIP = data.get('IIP') or iip.IIP
    iip.mining_industry = data.get('mining_industry') or iip.mining_industry 
    iip.manufacturing_processing_industry = data.get('manufacturing_processing_industry') or iip.manufacturing_processing_industry
    iip.gas_electricity_industry = data.get('gas_electricity_industry') or iip.gas_electricity_industry
    iip.waste_treatment_water_supply = data.get('waste_treatment_water_supply') or iip.waste_treatment_water_supply
    iip.mineral_exploitation = data.get('mineral_exploitation') or iip.mineral_exploitation
    iip.food = data.get('food') or iip.food
    iip.cigarette = data.get('cigarette') or iip.cigarette
    iip.textile = data.get('textile') or iip.textile
    iip.costume = data.get('costume') or iip.costume
    iip.leather_product = data.get('leather_product') or iip.leather_product
    iip.paper_product = data.get('paper_product') or iip.paper_product
    iip.chemical_product = data.get('chemical_product') or iip.chemical_product
    iip.plastic_product = data.get('plastic_product') or iip.plastic_product
    iip.non_metalic_mineral_product = data.get('non_metalic_mineral_product') or iip.non_metalic_mineral_product
    iip.prefabricated_metal_product = data.get('prefabricated_metal_product') or iip.prefabricated_metal_product
    iip.electrical_product = data.get('electrical_product') or iip.electrical_product
    iip.motor_vehicle = data.get('motor_vehicle') or iip.motor_vehicle
    iip.furniture = data.get('furniture') or iip.furniture
    iip.other_manufacturing_processing = data.get('other_manufacturing_processing') or iip.other_manufacturing_processing
    iip.water_supply = data.get('water_supply') or iip.water_supply
    iip.gas_electricity = data.get('gas_electricity') or iip.gas_electricity
    iip.other_products = data.get('other_products') or iip.other_products
    iip.base_period = data.get('base_period') or iip.base_period
    iip.save(update_fields=['IIP', 'mining_industry', 'manufacturing_processing_industry', 'gas_electricity_industry', 'waste_treatment_water_supply',
                            'mineral_exploitation', 'food', 'cigarette', 'textile', 'costume', 'leather_product', 'paper_product', 
                            'chemical_product', 'plastic_product', 'non_metalic_mineral_product', 'prefabricated_metal_product', 'electrical_product', 
                            'motor_vehicle', 'furniture', 'other_manufacturing_processing', 'water_supply', 'gas_electricity','other_products', 'base_period'])
    return iip

def delete_iip(iip):
    iip.delete()
    return iip
