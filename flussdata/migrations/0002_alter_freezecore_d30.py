# Generated by Django 4.0.5 on 2022-06-09 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flussdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freezecore',
            name='d30',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
