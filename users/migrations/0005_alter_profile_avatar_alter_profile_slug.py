# Generated by Django 4.1.7 on 2023-03-31 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_options_remove_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
