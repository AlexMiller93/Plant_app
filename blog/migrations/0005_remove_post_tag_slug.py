# Generated by Django 4.1.7 on 2023-04-13 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_tag_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag_slug',
        ),
    ]
