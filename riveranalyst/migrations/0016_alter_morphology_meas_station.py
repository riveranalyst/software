# Generated by Django 4.0.5 on 2023-04-06 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riveranalyst', '0015_alter_biota_meas_station_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='morphology',
            name='meas_station',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.measstation'),
        ),
    ]
