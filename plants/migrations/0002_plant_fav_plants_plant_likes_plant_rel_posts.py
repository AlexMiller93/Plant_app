# Generated by Django 4.1.7 on 2023-05-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_age'),
        ('blog', '0014_post_share_delete_share'),
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='fav_plants',
            field=models.ManyToManyField(blank=True, related_name='favorites_plants', to='users.profile'),
        ),
        migrations.AddField(
            model_name='plant',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='plant_like', to='users.profile'),
        ),
        migrations.AddField(
            model_name='plant',
            name='rel_posts',
            field=models.ManyToManyField(blank=True, related_name='plant_posts', to='blog.post'),
        ),
    ]