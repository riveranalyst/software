# Generated by Django 4.0.5 on 2022-09-08 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flussdata', '0006_alter_ido_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measstation',
            name='coord_system',
            field=models.CharField(help_text='The coordinate system is mandatory, please enter it as epsg number (eg., epsg:<epsg-code>).', max_length=15),
        ),
        migrations.AlterField(
            model_name='measstation',
            name='date',
            field=models.DateField(blank=True, help_text='Please use the following format: <em>DD.MM.YYYY</em>.', null=True, verbose_name='Date of measurement'),
        ),
        migrations.AlterField(
            model_name='measstation',
            name='name',
            field=models.CharField(help_text='Please use unique station names.', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='measstation',
            name='pos_rel_WB',
            field=models.FloatField(blank=True, help_text='use "+" for wetted and "-" for dry locations', null=True, verbose_name='Dist from wetted boundary [m]'),
        ),
    ]
