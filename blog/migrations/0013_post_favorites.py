# Generated by Django 4.1.7 on 2023-05-10 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_age'),
        ('blog', '0012_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorites', to='users.profile'),
        ),
    ]
