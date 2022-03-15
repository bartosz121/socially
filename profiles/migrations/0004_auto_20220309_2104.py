# Generated by Django 3.2.12 on 2022-03-09 21:04

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20220305_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_background',
            field=models.ImageField(default='profile_images/background_default.jpg', upload_to=profiles.models.profile_images_handler),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_images/profile_default.png', upload_to=profiles.models.profile_images_handler),
        ),
    ]
