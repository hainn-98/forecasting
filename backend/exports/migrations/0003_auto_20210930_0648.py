import os
from django.db import migrations
from django.conf import settings
import pandas as pd
from ..models import Export
from users.models import User


def initialize_export_data(apps, schema_editor):
    data_path = os.path.join(settings.BASE_DIR, 'utils/data/export_data.xlsx')
    indexes = ('export', 'domestic_economy', 'foreign_invested_economy', 'footwear', 'textile_product', 'wood_product', 'textile_yarn',
                'machinery_equipment', 'transport_vehicle', 'coffe', 'iron_steel_product', 'electronic_product',
                'cashew', 'plastic_product', 'pepper', 'rubber')
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
        Export.objects.create(**data_dict)

class Migration(migrations.Migration):

    dependencies = [
        ('exports', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_export_data),
    ]
