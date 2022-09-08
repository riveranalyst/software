# Generated by Django 4.0.5 on 2022-09-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flussdata', '0008_alter_ido_dp_position_alter_ido_meas_station_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sedsampltechnique',
            name='samp_techniques',
            field=models.CharField(choices=[('FC', 'Freeze Core'), ('OS', 'Surface Sample other (a.k.a. Overlayer Sediment sample)'), ('US', 'Subsurface Sample other (a.k.a. Underlayer Sediment sample)'), ('FP', 'Freeze Panel'), ('LS', 'Line Sampling')], max_length=200, null=True, verbose_name='Sediment Sampling Technique'),
        ),
    ]
