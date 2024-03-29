# Generated by Django 4.1.7 on 2023-11-01 16:48

from django.db import migrations, models
import plants.models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0007_remove_plant_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='latin_title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='picture',
            field=models.ImageField(blank=True, default='images/plant_default.png', null=True, upload_to=plants.models.picture_directory_path),
        ),
        migrations.AlterField(
            model_name='plant',
            name='real_images',
            field=models.ImageField(blank=True, height_field=100, help_text='Upload images with your plants', null=True, upload_to=plants.models.images_directory_path, width_field=200),
        ),
    ]
