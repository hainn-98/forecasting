import os
from django.db import migrations
from django.conf import settings
import pandas as pd
from ..models import Iip
from users.models import User


def initialize_iip_data(apps, schema_editor):
    data_path = os.path.join(settings.BASE_DIR, 'utils/data/iip_data.xlsx')
    indexes = ('IIP', 'mining_industry', 'manufacturing_processing_industry', 'gas_electricity_industry', 'waste_treatment_water_supply', 'mineral_exploitation', 'food', 'cigarette', 'textile', 'costume', 'leather_product', 'paper_product', 'chemical_product', 'plastic_product',
                'non_metalic_mineral_product', 'prefabricated_metal_product', 'electrical_product', 'other_products', 'motor_vehicle', 
                'furniture', 'other_manufacturing_processing', 'water_supply', 'gas_electricity')
    data = pd.read_excel(data_path, header=None)
    df = data.iloc[:, 1:]
    for time in range(df.shape[1]):
        data = df.iloc[:, time]
        year = data[0].year
        month = data[0].month
        data_dict = dict(zip(indexes, tuple(data[1:])))
        user = User.objects.filter(id=1).first()
        data_dict['year'] = year
        data_dict['month'] = month
        data_dict['creator'] = user
        data_dict['organization'] = user.client
        data_dict['base_period'] = 2014
        Iip.objects.create(**data_dict)

class Migration(migrations.Migration):

    dependencies = [
        ('iips', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_iip_data),
    ]
