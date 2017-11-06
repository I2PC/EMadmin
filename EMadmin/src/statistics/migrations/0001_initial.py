# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('create_proj', '0003_auto_20171105_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberMovies', models.IntegerField(default=-1)),
                ('averageResolution', models.FloatField(default=-1)),
                ('resolutionData', models.TextField()),
                ('acquisition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='create_proj.Acquisition')),
            ],
        ),
    ]
