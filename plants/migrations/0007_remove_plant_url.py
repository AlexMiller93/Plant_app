# Generated by Django 4.1.7 on 2023-10-31 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0006_plant_url_alter_plant_likes_alter_plant_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='url',
        ),
    ]
