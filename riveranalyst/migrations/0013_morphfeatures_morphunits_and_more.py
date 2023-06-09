# Generated by Django 4.0.5 on 2022-09-16 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riveranalyst', '0012_survey_remove_measstation_campaign_delete_campaign_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MorphFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MorphUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hydraulics',
            name='turbidity_ntu',
        ),
        migrations.AddField(
            model_name='hydraulics',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='kf',
            name='slurp_rate_avg_mls',
            field=models.FloatField(blank=True, null=True, verbose_name='Slurping rate [mg/l]'),
        ),
        migrations.AlterField(
            model_name='subsurfacesed',
            name='geom_std_grain',
            field=models.FloatField(blank=True, null=True, verbose_name='Geom. Std of grains'),
        ),
        migrations.AlterField(
            model_name='subsurfacesed',
            name='n_wu_wang',
            field=models.FloatField(blank=True, null=True, verbose_name='Porosity (Wu & Wang, 2006) [-]'),
        ),
        migrations.AlterField(
            model_name='surfacesed',
            name='geom_std_grain',
            field=models.FloatField(blank=True, null=True, verbose_name='Geom. std of grains'),
        ),
        migrations.AlterField(
            model_name='surfacesed',
            name='n_wu_wang',
            field=models.FloatField(blank=True, null=True, verbose_name='Porosity (Wu & Wang, 2006) [-]'),
        ),
        migrations.CreateModel(
            name='WaterQual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(max_length=200)),
                ('ph', models.FloatField(blank=True, null=True, verbose_name='pH [-]')),
                ('cod', models.FloatField(blank=True, null=True, verbose_name='COD [mg/l]')),
                ('bod', models.FloatField(blank=True, null=True, verbose_name='BOD [mg/l]')),
                ('turbidity_ntu', models.FloatField(blank=True, null=True, verbose_name='Turbidity [NTU]')),
                ('temp_c', models.FloatField(blank=True, null=True, verbose_name='Temperature [°C]')),
                ('do_mgl', models.FloatField(blank=True, null=True, verbose_name='Dissolved oxygen concentration [mg/l]')),
                ('do_sat', models.FloatField(blank=True, null=True, verbose_name='Dissolved oxygen saturation [%]')),
                ('no_3', models.FloatField(blank=True, null=True, verbose_name='NO-3 [mg/l]')),
                ('meas_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.measstation', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Morphology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(max_length=200)),
                ('meas_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.measstation', unique=True)),
                ('morphological_features', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.morphfeatures')),
                ('morphological_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.morphunits')),
            ],
        ),
        migrations.CreateModel(
            name='Biota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(max_length=200)),
                ('count_macrozoobenthos', models.IntegerField(blank=True, null=True, verbose_name='Macrozoobenthos count')),
                ('planting_species', models.CharField(blank=True, max_length=200, null=True)),
                ('meas_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riveranalyst.measstation', unique=True)),
            ],
        ),
    ]
