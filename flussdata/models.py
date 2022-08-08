from django.db import models


# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.utils import timezone
# import pandas as pd


class River(models.Model):
    river = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.river


class Campaign(models.Model):
    campaign = models.CharField(max_length=200)

    def __str__(self):
        return self.campaign


class CollectedData(models.Model):
    DATACOLLECTION = (
        ('IDOC', 'Intragravel Dissolved Oxygen Content'),
        ('kf', 'Hydraulic Conductivity'),
        ('SurfSed', 'Surface Sediment Sampling'),
        ('SubsurfSed', 'Subsurface Sediment Sampling'),
        ('Hydraulics', 'FlowTracker')
    )
    collected_data = models.CharField(max_length=200, null=True, choices=DATACOLLECTION)

    def __str__(self):
        return self.collected_data


class SedSamplTechnique(models.Model):
    TECHNIQUES = (
        ('FC', 'Freeze Core'),
        ('OS', 'Overlayer Sample'),
        ('US', 'Underlayer Sample'),
        ('FP', 'Freeze Panel'),
        ('LS', 'Line Sampling'),
    )
    samp_techniques = models.CharField(max_length=200, null=True,
                                       choices=TECHNIQUES, verbose_name='Sediment Sampling Technique')

    def __str__(self):
        return self.samp_techniques


class MeasStation(models.Model):
    name = models.CharField(max_length=100, default='to fill')
    river = models.ForeignKey(River, on_delete=models.SET_NULL, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)
    collected_data = models.ManyToManyField(CollectedData)
    date = models.DateField('date of measurement', null=True, blank=True)  # 'date of measureemnt' is the verbose name (optional arg)
    description = models.CharField(max_length=400, null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    wl_m = models.FloatField(null=True, blank=True, verbose_name='Water Level [m]')
    H_m = models.FloatField(null=True, blank=True, verbose_name='H [m]')

    def __str__(self):
        return self.name


class SubsurfaceSed(models.Model):
    meas_station = models.ForeignKey(MeasStation, verbose_name='Measurement station', on_delete=models.SET_NULL,
                                     null=True)
    sample_id = models.CharField(max_length=200)
    sampling_method = models.ForeignKey(SedSamplTechnique, on_delete=models.SET_NULL, null=True)
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

    # class Meta:
    #     ordering = ['date']

    def __str__(self):
        object_descrip = "{}".format(self.sample_id)
        return object_descrip


class SurfaceSed(models.Model):
    # Sample class definition as SubsurfaceSeb but without the attribute of porosity from Structure from Motion

    meas_station = models.ForeignKey(MeasStation, verbose_name='Measurement station', on_delete=models.SET_NULL,
                                     null=True)
    sample_id = models.CharField(max_length=200)
    sampling_method = models.ForeignKey(SedSamplTechnique, on_delete=models.SET_NULL, null=True)
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

    # class Meta:
    #     ordering = ['date']

    def __str__(self):
        object_descrip = "{}".format(self.sample_id)
        return object_descrip


class IDOC(models.Model):
    meas_station = models.ForeignKey(MeasStation, verbose_name='Measurement station', on_delete=models.SET_NULL, null=True)
    sample_id = models.CharField(max_length=200)
    dp_position = models.IntegerField(null=True, blank=True, verbose_name='DP Position [-]')
    sediment_depth_m = models.FloatField(null=True, verbose_name='Sediment Depth [m]')
    idoc_mgl = models.FloatField(null=True, blank=True, verbose_name='IDOC [mg/l]',)
    temp_c = models.FloatField(null=True, blank=True, verbose_name='Temperature [C°]')
    idoc_sat = models.FloatField(null=True, blank=True, verbose_name='IDOS [%]')
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.sample_id


class Kf(models.Model):
    meas_station = models.ForeignKey(MeasStation, on_delete=models.SET_NULL, null=True)
    sample_id = models.CharField(max_length=200)
    dp_position = models.IntegerField(null=True, blank=True)
    sediment_depth_m = models.FloatField(null=True)
    kf_ms = models.FloatField(null=True, blank=True)
    slurp_rate_avg_mls = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.sample_id


class Flow(models.Model):
    meas_station = models.ForeignKey(MeasStation, on_delete=models.SET_NULL, null=True)
    sample_id = models.CharField(max_length=200)
    v_x = models.FloatField(null=True, blank=True, verbose_name='v_x [m/s]')
    v_y = models.FloatField(null=True, blank=True, verbose_name='v_y [m/s]')
    v_z = models.FloatField(null=True, blank=True, verbose_name='v_z [m/s]')
    kt_norm = models.FloatField(null=True, blank=True, verbose_name='kt/U² [-]')
    kt_2d_norm = models.FloatField(null=True, blank=True, verbose_name='kt 2d/U² [-]')
    discharge = models.FloatField(null=True, blank=True, verbose_name='Q [m³/s]')