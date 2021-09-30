from .models import Import
from utils.custom_exceptions import *


def get_import_by(raise_exception=True, **kwargs):
    _import = Import.objects.filter(**kwargs).all()
    if not _import and raise_exception: 
        raise ObjectNotFound
    return _import

def add_import(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    _import = get_import_by(raise_exception=False,  year=data['year'], month = data['month']).first()
    if _import:
        raise DuplicateEntry(entry=str(_import.year) + str(_import.month), key='year and month')
    _import = Import.objects.create(**dict(data))
    return _import

def update_import(_import, data):
    if not any(data.values()):
        raise ValidationError
    _import._import = data.get('_import') or _import._import
    _import.domestic_economy = data.get('domestic_economy') or _import.domestic_economy
    _import.foreign_invested_economy = data.get('foreign_invested_economy') or _import.foreign_invested_economy
    _import.machinery_equipment = data.get('machinery_equipment') or _import.machinery_equipment
    _import.plastic_material = data.get('plastic_material') or _import.plastic_material
    _import.cashew = data.get('cashew') or _import.cashew
    _import.rubber = data.get('rubber') or _import.rubber
    _import.cloth = data.get('cloth') or _import.cloth
    _import.iron_steel = data.get('iron_steel') or _import.iron
    _import.animal_feed = data.get('animal_feed') or _import.animal_feed
    _import.chemical = data.get('chemical') or _import.chemical
    _import.textile_material = data.get('textile_material') or _import.textile_material
    _import.metal = data.get('metal') or _import.metal
    _import.corn = data.get('corn') or _import.corn
    _import.chemical_product = data.get('chemical_product') or _import.chemical_product 
    _import.textile_yarn = data.get('textile_yarn') or _import.textile_yarn
    _import.electronic_product = data.get('electronic_product') or _import.electronic_product
    _import.cotton = data.get('cotton') or _import.cotton
    _import.pesticide = data.get('pesticide') or _import.pesticide
    _import.wood_product = data.get('wood_product') or _import.wood_product
    _import.medicine = data.get('medicine') or _import.medicine
    _import.save(update_fields=['_import', 'domestic_economy', 'foreign_invested_economy', 'machinery_equipment',
                                'plastic_material', 'cashew', 'rubber', 'cloth', 'iron_steel', 'chemical', 'animal_feed',
                                'textile_material', 'metal', 'corn', 'chemical_product', 'textile_yarn', 'electronic_product',
                                'cotton', 'pesticide', 'wood_product', 'medicine'])
    return _import

def delete_import(_import):
    _import.delete()
    return _import
