# Generated by Django 4.1.7 on 2023-10-26 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_remove_post_tag_post_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tag',
            new_name='tags',
        ),
    ]