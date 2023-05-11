# Generated by Django 4.1.7 on 2023-05-09 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_age'),
        ('blog', '0011_alter_comment_author_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_like', to='users.profile'),
        ),
    ]