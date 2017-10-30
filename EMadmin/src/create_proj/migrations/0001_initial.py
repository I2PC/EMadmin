# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 22:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acquisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.CharField(max_length=128)),
                ('voltage', models.IntegerField(default=200)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('shiftLength', models.FloatField(default=3)),
                ('projname', models.CharField(blank=True, max_length=128, unique=True)),
                ('backupPath', models.CharField(blank=True, default='NOBACKUP', max_length=128)),
                ('multiple_backup', models.BooleanField(default=False)),
                ('schedule', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Acquisition2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominal_magnification', models.FloatField()),
                ('sampling_rate', models.FloatField()),
                ('spotsize', models.FloatField()),
                ('illuminated_area', models.FloatField(blank=True, default=1.68)),
                ('dose_per_fraction', models.FloatField()),
                ('total_exposure_time', models.FloatField()),
                ('number_of_fractions', models.PositiveIntegerField()),
                ('frames_in_fraction', models.PositiveIntegerField()),
                ('nominal_defocus_range', models.CharField(default='array of floats', max_length=128)),
                ('autofocus_distance', models.FloatField()),
                ('drift_meassurement', models.CharField(choices=[('never', 'never'), ('always', 'always'), ('gridsquare', 'gridsquare')], default='never', max_length=16)),
                ('delay_after_stage_shift', models.IntegerField(default=5)),
                ('delay_after_image_shift', models.IntegerField(default=5)),
                ('max_image_shift', models.IntegerField(default=5)),
                ('exposure_hole', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=1)),
                ('c2', models.IntegerField(choices=[(30, '30'), (50, '50'), (70, '70'), (150, '150')], default=50)),
                ('o1', models.IntegerField(choices=[(30, '30'), (70, '70')], default=70)),
                ('php', models.IntegerField(choices=[(0, '--'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], default=3)),
                ('acquisition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='create_proj.Acquisition')),
            ],
        ),
        migrations.CreateModel(
            name='Microscope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('model', models.CharField(max_length=128, unique=True)),
                ('detector', models.CharField(default='FalconIII', max_length=64, unique=True)),
                ('detectorPixelSize', models.FloatField(default=14)),
                ('cs', models.FloatField(default=2.7)),
                ('dataFolder', models.CharField(default='/home/scipionuser/OffloadData', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('workflow', models.TextField(unique=True)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='acquisition',
            name='microscope',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='create_proj.Microscope'),
        ),
        migrations.AddField(
            model_name='acquisition',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acquisition',
            name='workflow',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='create_proj.Workflow'),
        ),
    ]
