# Generated by Django 4.1.7 on 2023-04-25 17:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_alter_comment_options_rename_text_comment_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='seen_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
