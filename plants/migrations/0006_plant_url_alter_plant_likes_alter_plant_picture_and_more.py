# Generated by Django 4.1.7 on 2023-10-31 09:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_alter_profile_avatar_alter_profile_sex'),
        ('plants', '0005_alter_plant_seen_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='url',
            field=models.URLField(default='2023-10-31'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plant',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='plant_likes', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='picture',
            field=models.ImageField(blank=True, default='images/plant_default.png', null=True, upload_to='images/users/{ user.username }/plants/picture/'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='real_images',
            field=models.ImageField(blank=True, height_field=100, help_text='Upload images with your plants', null=True, upload_to='images/users/{ user.username }/plants/images/', width_field=200),
        ),
        migrations.AlterField(
            model_name='plant',
            name='seen_by',
            field=models.ManyToManyField(related_name='plant_views', to=settings.AUTH_USER_MODEL),
        ),
    ]
