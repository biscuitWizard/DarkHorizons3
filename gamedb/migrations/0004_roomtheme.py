# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamedb', '0003_bankaccount_vehicleclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_theme_key', models.CharField(max_length=32)),
                ('db_descriptor_type', models.IntegerField()),
                ('db_descriptor', models.CharField(max_length=16)),
            ],
        ),
    ]
