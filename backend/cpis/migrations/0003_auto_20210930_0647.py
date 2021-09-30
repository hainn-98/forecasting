import os
from django.db import migrations
from django.conf import settings
import pandas as pd
from ..models import Cpi
from users.models import User


def initialize_cpi_data(apps, schema_editor):
    data_path = os.path.join(settings.BASE_DIR, 'utils/data/cpi_data.xlsx')
    indexes = ('CPI', 'food_service', 'cereal', 'food', 'eating_out', 'beverage_cigarette', 'garment', 'housing', 'household_equipment', 'medicine_medical_service', 'communication', 'telecommunication', 'education', 'culture_entertainment_travel', 'other_good_services')
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
        Cpi.objects.create(**data_dict)

class Migration(migrations.Migration):

    dependencies = [
        ('cpis', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_cpi_data),
    ]
