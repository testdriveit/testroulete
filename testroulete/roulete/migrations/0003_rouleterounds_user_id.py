# Generated by Django 3.2.13 on 2022-06-30 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roulete', '0002_rouleterounds'),
    ]

    operations = [
        migrations.AddField(
            model_name='rouleterounds',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
