# Generated by Django 4.0.5 on 2022-06-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Freezecore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('river', models.CharField(max_length=100)),
                ('sample_id', models.CharField(max_length=200)),
                ('sample_name', models.CharField(max_length=200)),
                ('site_name', models.CharField(max_length=150)),
                ('date', models.DateField(verbose_name='date of measurement')),
                ('time_stamp', models.CharField(max_length=150)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('porosity_sfm', models.FloatField(blank=True, null=True)),
                ('dm', models.FloatField(blank=True, null=True)),
                ('dg', models.FloatField(blank=True, null=True)),
                ('fi', models.FloatField(blank=True, null=True)),
                ('geom_std_grain', models.FloatField(blank=True, null=True)),
                ('d10', models.FloatField(blank=True, null=True)),
                ('d16', models.FloatField(blank=True, null=True)),
                ('d25', models.FloatField(blank=True, null=True)),
                ('d30', models.FloatField(blank=True, null=True)),
                ('d50', models.FloatField(blank=True, null=True)),
                ('d60', models.FloatField(blank=True, null=True)),
                ('d75', models.FloatField(blank=True, null=True)),
                ('d84', models.FloatField(blank=True, null=True)),
                ('d90', models.FloatField(blank=True, null=True)),
                ('cu', models.FloatField(blank=True, null=True)),
                ('cc', models.FloatField(blank=True, null=True)),
                ('fsf_le_2mm', models.FloatField(blank=True, null=True)),
                ('fsf_le_1mm', models.FloatField(blank=True, null=True)),
                ('fsf_le_0_5mm', models.FloatField(blank=True, null=True)),
                ('so', models.FloatField(blank=True, null=True)),
                ('wl_slurp_m', models.FloatField(blank=True, null=True)),
                ('wl_model_m', models.FloatField(blank=True, null=True)),
                ('n_wooster', models.FloatField(blank=True, null=True)),
                ('bed_slope', models.FloatField(blank=True, null=True)),
                ('comment', models.CharField(max_length=1000)),
                ('percent_finer_250mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_125mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_63mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_31_5mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_16mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_8mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_4mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_2mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_1mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_0_5mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_0_25mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_0_125mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_0_063mm', models.FloatField(blank=True, null=True)),
                ('percent_finer_0_031mm', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
