# Generated by Django 3.2.18 on 2023-06-19 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riveranalyst', '0017_auto_20230614_1305'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MeasStation',
            new_name='MeasPosition',
        ),
        migrations.RenameField(
            model_name='biota',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='hydraulics',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='ido',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='kf',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='morphology',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='subsurfacesed',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='surfacesed',
            old_name='meas_station',
            new_name='meas_position',
        ),
        migrations.RenameField(
            model_name='waterqual',
            old_name='meas_station',
            new_name='meas_position',
        ),
    ]
