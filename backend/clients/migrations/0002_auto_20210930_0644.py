from django.db import migrations
from ..services import *
from django.conf import settings


def initialize_client(apps, schema_editor):
    client_data = {'email': settings.EMAIL_TEST, 'client_name':'client1', 'address':'HN', 'name': 'client1_name'}
    client = create_client(data=client_data)

class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_client),
    ]
