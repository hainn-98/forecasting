# Generated by Django 3.2.5 on 2021-08-05 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_tokens', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoken',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
