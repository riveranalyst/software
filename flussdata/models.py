from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import pandas as pd


class Freezecore(models.Model):
    river = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=200)
    sample_name = models.CharField(max_length=200)
    site_name = models.CharField(max_length=150)
    date = models.DateField('date of measurement')
    time_stamp = models.CharField(max_length=150)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    porosity_sfm = models.FloatField(null=True, blank=True)
    dm = models.FloatField(null=True, blank=True)
    dg = models.FloatField(null=True, blank=True)
    fi = models.FloatField(null=True, blank=True)
    geom_std_grain = models.FloatField(null=True, blank=True)
    d10 = models.FloatField(null=True, blank=True)
    d16 = models.FloatField(null=True, blank=True)
    d25 = models.FloatField(null=True, blank=True)
    d30 = models.FloatField(null=True, blank=True)
    d50 = models.FloatField(null=True, blank=True)
    d60 = models.FloatField(null=True, blank=True)
    d75 = models.FloatField(null=True, blank=True)
    d84 = models.FloatField(null=True, blank=True)
    d90 = models.FloatField(null=True, blank=True)
    cu = models.FloatField(null=True, blank=True)
    cc = models.FloatField(null=True, blank=True)
    fsf_le_2mm = models.FloatField(null=True, blank=True)
    fsf_le_1mm = models.FloatField(null=True, blank=True)
    fsf_le_0_5mm = models.FloatField(null=True, blank=True)
    so = models.FloatField(null=True, blank=True)
    wl_slurp_m = models.FloatField(null=True, blank=True)
    wl_model_m = models.FloatField(null=True, blank=True)
    n_wooster = models.FloatField(null=True, blank=True)
    bed_slope = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=1000)
    percent_finer_250mm = models.FloatField(null=True, blank=True)
    percent_finer_125mm = models.FloatField(null=True, blank=True)
    percent_finer_63mm = models.FloatField(null=True, blank=True)
    percent_finer_31_5mm = models.FloatField(null=True, blank=True)
    percent_finer_16mm = models.FloatField(null=True, blank=True)
    percent_finer_8mm = models.FloatField(null=True, blank=True)
    percent_finer_4mm = models.FloatField(null=True, blank=True)
    percent_finer_2mm = models.FloatField(null=True, blank=True)
    percent_finer_1mm = models.FloatField(null=True, blank=True)
    percent_finer_0_5mm = models.FloatField(null=True, blank=True)
    percent_finer_0_25mm = models.FloatField(null=True, blank=True)
    percent_finer_0_125mm = models.FloatField(null=True, blank=True)
    percent_finer_0_063mm = models.FloatField(null=True, blank=True)
    percent_finer_0_031mm = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        object_descrip = "{} ({})".format(self.sample_id, self.river)
        return object_descrip


class VertiCo(models.Model):
    river = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=200)
    sample_name = models.CharField(max_length=200)
    site_name = models.CharField(max_length=150)
    date = models.DateField('date of measurement', blank=True)
    time_stamp = models.CharField(max_length=150)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    dp_position = models.IntegerField(null=True, blank=True)
    sediment_depth_m = models.FloatField(null=True)
    wl_m = models.FloatField(null=True, blank=True)
    H_m = models.FloatField(null=True, blank=True)
    slurp_rate_avg_mls = models.FloatField(null=True, blank=True)
    idoc_mgl = models.FloatField(null=True, blank=True)
    temp_c = models.FloatField(null=True, blank=True)
    idoc_sat = models.FloatField(null=True, blank=True)
    kf_ms = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=1000)

    fc_sample = models.ManyToManyField(Freezecore)


