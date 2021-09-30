from .models import Export
from utils.custom_exceptions import *


def get_export_by(raise_exception=True, **kwargs):
    export = Export.objects.filter(**kwargs).all()
    if not export and raise_exception: 
        raise ObjectNotFound
    return export

def add_export(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    export = get_export_by(raise_exception=False,  year=data['year'], month = data['month']).first()
    if export:
        raise DuplicateEntry(entry=str(export.year) + str(export.month), key='year and month')
    export = Export.objects.create(**dict(data))
    return export

def update_export(export, data):
    if not any(data.values()):
        raise ValidationError
    export.export = data.get('export') or export.export
    export.domestic_economy = data.get('domestic_economy') or export.domestic_economy
    export.foreign_invested_economy = data.get('foreign_invested_economy') or export.foreign_invested_economy
    export.footwear = data.get('footwear') or export.footwear
    export.textile_product = data.get('textile_product') or export.textile_product
    export.textile_yarn = data.get('textile_yarn') or export.textile_yarn
    export.wood_product = data.get('wood_product') or export.wood_product
    export.machinery_equipment = data.get('machinery_equipment') or export.machinery_equipment
    export.transport_vehicle = data.get('transport_vehicle') or export.transport_vehicle
    export.coffe = data.get('coffe') or export.coffe
    export.iron_steel_product = data.get('iron_steel_product') or export.iron_steel_product
    export.electronic_product = data.get('electronic_product') or export.electronic_product
    export.cashew = data.get('cashew') or export.cashew
    export.plastic_product = data.get('plastic_product') or export.plastic_product
    export.pepper = data.get('pepper') or export.pepper
    export.rubber = data.get('rubber') or export.rubber
    export.save(update_fields=['export', 'domestic_economy', 'foreign_invested_economy', 'footwear', 'textile_product', 'textile_yarn',
                                'wood_product', 'machinery_equipment', 'transport_vehicle', 'coffe', 'iron_steel_product', 'electronic_product',
                                'cashew', 'plastic_product', 'pepper', 'rubber'])
    return export

def delete_export(export):
    export.delete()
    return export
