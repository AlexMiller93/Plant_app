# Generated by Django 4.1.7 on 2023-05-18 11:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plants', '0004_plant_seen_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='seen_by',
            field=models.ManyToManyField(related_name='plant_view', to=settings.AUTH_USER_MODEL),
        ),
    ]
