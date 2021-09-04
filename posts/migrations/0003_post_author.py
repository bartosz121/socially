# Generated by Django 3.2.6 on 2021-09-04 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('posts', '0002_auto_20210904_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='profiles.profile'),
        ),
    ]
