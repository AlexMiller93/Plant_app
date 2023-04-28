# Generated by Django 4.1.7 on 2023-04-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_rating_profile_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=4, null=True),
        ),
    ]