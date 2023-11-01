# Generated by Django 4.1.7 on 2023-11-01 17:29

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_profile_avatar_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/default.png', null=True, upload_to=users.models.avatar_directory_path),
        ),
    ]
