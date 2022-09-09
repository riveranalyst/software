from django.db import models


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
        ('IDO', 'Intragravel Dissolved Oxygen'),
        ('kf', 'Hydraulic Conductivity'),
        ('SurfSed', 'Surface Sediment Sampling'),
        ('SubsurfSed', 'Subsurface Sediment Sampling'),
        ('Hydraulics', 'FlowTracker'),
        #TODO cretae model for vegetation mapping
        # ('Abiotic', 'Abiotic elements'),
        # ('Biotic', 'Biotic Elements'),
        # ('WaterQual', 'Water Quality')
    )
    collected_data = models.CharField(max_length=200, null=True,
                                      choices=DATACOLLECTION,
                                      verbose_name='Measurement Data')

    def __str__(self):
        return self.collected_data


class SedSamplTechnique(models.Model):
    TECHNIQUES = (
        ('FC', 'Freeze Core'),
        ('OS', 'Surface Sample other (a.k.a. Overlayer Sediment sample)'),
        ('US', 'Subsurface Sample other (a.k.a. Underlayer Sediment sample)'),
        ('FP', 'Freeze Panel'),
        ('LS', 'Line Sampling'),
    )
    samp_techniques = models.CharField(max_length=200, null=True,
                                       choices=TECHNIQUES, verbose_name='Sediment Sampling Technique')

    def __str__(self):
        return self.samp_techniques


class MeasStation(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Please use unique station names.")
    river = models.ForeignKey(River, on_delete=models.SET_NULL, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)
    collected_data = models.ManyToManyField(CollectedData)
    date = models.DateField('Date of measurement', null=True, blank=True,
                            help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    description = models.CharField(max_length=400, null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    x_epsg4326 = models.FloatField(null=True, blank=True)
    y_epsg4326 = models.FloatField(null=True, blank=True)
    bed_elevation_wgs84 = models.FloatField(null=True, blank=True)
    bed_elevation_dhhn = models.FloatField(null=True, blank=True)
    coord_system = models.CharField(max_length=15,
                                    null=True,
                                    blank=True,
                                    help_text='The coordinate system is mandatory, please enter it as '
                                                             'epsg number (eg., epsg:<epsg-code>).')
    pos_rel_WB = models.FloatField(null=True, blank=True,
                                   verbose_name='Dist from wetted boundary [m]',
                                   help_text='use "+" for wetted and "-" for dry locations')
    discharge = models.FloatField(null=True, blank=True,
                                  verbose_name='Discharge at recording time [m³/s]')
    wl_m = models.FloatField(null=True, blank=True, verbose_name='Water level measured in-situ at recording time [m]')
    wl_model_m = models.FloatField(null=True, blank=True, verbose_name='Modelled water level [m]')
    ALGAE = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('BLANK', 'Blank'),
    )
    algae_cover = models.CharField(null=True, max_length=100, choices=ALGAE, blank=True)
    IMBRI = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('BLANK', 'Blank'),
    )
    imbrication = models.CharField(null=True, max_length=100, choices=IMBRI, blank=True)
    bed_slope = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubsurfaceSed(models.Model):
    # many-to-one relationship (many SubsurfaceSeds to one MeasStation)
    meas_station = models.ForeignKey(MeasStation,
                                     verbose_name='Measurement station',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     help_text='This field will be used to link the parametrical data tables'
                                               'to a given measurement point.')
    sample_id = models.CharField(max_length=200,
                                 help_text='This field is used to differentiate between duplicate '
                                           'measurements performed in the same station.')
    sampling_method = models.ForeignKey(SedSamplTechnique,
                                        on_delete=models.SET_NULL,
                                        null=True)
    operator_name = models.CharField(null=True,
                                     blank=True,
                                     max_length=100)

    # Actual variables
    dm = models.FloatField(null=True, blank=True, verbose_name='Dm (Mean grain size) [mm]')
    dg = models.FloatField(null=True, blank=True, verbose_name='Dg (Geom. Mean Grain size) [mm]')
    fi = models.FloatField(null=True, blank=True, verbose_name='Fredle Index [-]')
    std_grain = models.FloatField(null=True, blank=True, verbose_name='Grain size std')
    geom_std_grain = models.FloatField(null=True, blank=True, verbose_name='Dg (Geom. Std of grains)')
    skewness = models.FloatField(null=True, blank=True)
    kurtosis = models.FloatField(null=True, blank=True)
    cu = models.FloatField(null=True, blank=True, verbose_name='Coefficient of uniformity [-]')
    cc = models.FloatField(null=True, blank=True, verbose_name='Curvature coefficient [-]')
    n_carling = models.FloatField(null=True, blank=True, verbose_name='Porosity (Carling & Reader, 1982) [-]')
    n_wu_wang = models.FloatField(null=True, blank=True, verbose_name='Porosity (Wu & Wang, 206) [-]')
    n_wooster = models.FloatField(null=True, blank=True, verbose_name='Porosity (Wooster et al., 2008) [-]')
    n_frings = models.FloatField(null=True, blank=True, verbose_name='Porosity (Frings et al., 2011) [-]')
    n_user = models.FloatField(null=True, blank=True, verbose_name='Porosity (Seitz et al., 2018) [-]')
    d10 = models.FloatField(null=True, blank=True, verbose_name='D10 [mm]')
    d16 = models.FloatField(null=True, blank=True, verbose_name='D16 [mm]')
    d25 = models.FloatField(null=True, blank=True, verbose_name='D25 [mm]')
    d30 = models.FloatField(null=True, blank=True, verbose_name='D30 [mm]')
    d50 = models.FloatField(null=True, blank=True, verbose_name='D50 [mm]')
    d60 = models.FloatField(null=True, blank=True, verbose_name='D60 [mm]')
    d75 = models.FloatField(null=True, blank=True, verbose_name='D75 [mm]')
    d84 = models.FloatField(null=True, blank=True, verbose_name='D84 [mm]')
    d90 = models.FloatField(null=True, blank=True, verbose_name='D90 [mm]')
    so = models.FloatField(null=True, blank=True, verbose_name='Sorting coefficient (Bunte & Abt, 2001) [-]')
    comment = models.CharField(max_length=1000, null=True, blank=True)
    percent_finer_250mm = models.FloatField(null=True, blank=True, verbose_name='<250 mm [%]')
    percent_finer_125mm = models.FloatField(null=True, blank=True, verbose_name='<125 mm [%]')
    percent_finer_63mm = models.FloatField(null=True, blank=True, verbose_name='<63 mm [%]')
    percent_finer_31_5mm = models.FloatField(null=True, blank=True, verbose_name='<31.5 mm [%]')
    percent_finer_16mm = models.FloatField(null=True, blank=True, verbose_name='<16 mm [%]')
    percent_finer_8mm = models.FloatField(null=True, blank=True, verbose_name='<8 mm [%]')
    percent_finer_4mm = models.FloatField(null=True, blank=True, verbose_name='<4 mm [%]')
    percent_finer_2mm = models.FloatField(null=True, blank=True, verbose_name='<2 mm [%]')
    percent_finer_1mm = models.FloatField(null=True, blank=True, verbose_name='<1 mm [%]')
    percent_finer_0_5mm = models.FloatField(null=True, blank=True, verbose_name='<0.5 mm [%]')
    percent_finer_0_25mm = models.FloatField(null=True, blank=True, verbose_name='<0.25 mm [%]')
    percent_finer_0_125mm = models.FloatField(null=True, blank=True, verbose_name='<0.125 mm [%]')
    percent_finer_0_063mm = models.FloatField(null=True, blank=True, verbose_name='<0.063 mm [%]')
    percent_finer_0_031mm = models.FloatField(null=True, blank=True, verbose_name='<0.031 mm [%]')

    def __str__(self):
        object_descrip = "{}".format(self.sample_id)
        return object_descrip


class SurfaceSed(models.Model):
    # Sample class definition as SubsurfaceSeb but without the attribute of porosity from Structure from Motion
    # many-to-one relationship (many SurfaceSeds to one MeasStation)
    meas_station = models.ForeignKey(MeasStation, verbose_name='Measurement station',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     help_text='This field will be used to link the parametrical data tables'
                                               'to a given measurement point.')
    sample_id = models.CharField(max_length=200)
    sampling_method = models.ForeignKey(SedSamplTechnique, on_delete=models.SET_NULL, null=True)
    operator_name = models.CharField(null=True, blank=True, max_length=100)

    # Actual variables
    dm = models.FloatField(null=True, blank=True, verbose_name='Dm (Mean grain size) [mm]')
    dg = models.FloatField(null=True, blank=True, verbose_name='Dg (Geom. Mean Grain size) [mm]')
    fi = models.FloatField(null=True, blank=True, verbose_name='Fredle Index [-]')
    std_grain = models.FloatField(null=True, blank=True, verbose_name='Grain size std')
    geom_std_grain = models.FloatField(null=True, blank=True, verbose_name='Dg (Geom. Std of grains)')
    skewness = models.FloatField(null=True, blank=True)
    kurtosis = models.FloatField(null=True, blank=True)
    cu = models.FloatField(null=True, blank=True, verbose_name='Coefficient of uniformity [-]')
    cc = models.FloatField(null=True, blank=True, verbose_name='Curvature coefficient [-]')
    n_carling = models.FloatField(null=True, blank=True, verbose_name='Porosity (Carling & Reader, 1982) [-]')
    n_wu_wang = models.FloatField(null=True, blank=True, verbose_name='Porosity (Wu & Wang, 206) [-]')
    n_wooster = models.FloatField(null=True, blank=True, verbose_name='Porosity (Wooster et al., 2008) [-]')
    n_frings = models.FloatField(null=True, blank=True, verbose_name='Porosity (Frings et al., 2011) [-]')
    n_user = models.FloatField(null=True, blank=True, verbose_name='Porosity (Seitz et al., 2018) [-]')
    d10 = models.FloatField(null=True, blank=True, verbose_name='D10 [mm]')
    d16 = models.FloatField(null=True, blank=True, verbose_name='D16 [mm]')
    d25 = models.FloatField(null=True, blank=True, verbose_name='D25 [mm]')
    d30 = models.FloatField(null=True, blank=True, verbose_name='D30 [mm]')
    d50 = models.FloatField(null=True, blank=True, verbose_name='D50 [mm]')
    d60 = models.FloatField(null=True, blank=True, verbose_name='D60 [mm]')
    d75 = models.FloatField(null=True, blank=True, verbose_name='D75 [mm]')
    d84 = models.FloatField(null=True, blank=True, verbose_name='D84 [mm]')
    d90 = models.FloatField(null=True, blank=True, verbose_name='D90 [mm]')
    so = models.FloatField(null=True, blank=True, verbose_name='Sorting coefficient (Bunte & Abt, 2001) [-]')
    comment = models.CharField(max_length=1000, null=True, blank=True)
    percent_finer_250mm = models.FloatField(null=True, blank=True, verbose_name='<250 mm [%]')
    percent_finer_125mm = models.FloatField(null=True, blank=True, verbose_name='<125 mm [%]')
    percent_finer_63mm = models.FloatField(null=True, blank=True, verbose_name='<63 mm [%]')
    percent_finer_31_5mm = models.FloatField(null=True, blank=True, verbose_name='<31.5 mm [%]')
    percent_finer_16mm = models.FloatField(null=True, blank=True, verbose_name='<16 mm [%]')
    percent_finer_8mm = models.FloatField(null=True, blank=True, verbose_name='<8 mm [%]')
    percent_finer_4mm = models.FloatField(null=True, blank=True, verbose_name='<4 mm [%]')
    percent_finer_2mm = models.FloatField(null=True, blank=True, verbose_name='<2 mm [%]')
    percent_finer_1mm = models.FloatField(null=True, blank=True, verbose_name='<1 mm [%]')
    percent_finer_0_5mm = models.FloatField(null=True, blank=True, verbose_name='<0.5 mm [%]')
    percent_finer_0_25mm = models.FloatField(null=True, blank=True, verbose_name='<0.25 mm [%]')
    percent_finer_0_125mm = models.FloatField(null=True, blank=True, verbose_name='<0.125 mm [%]')
    percent_finer_0_063mm = models.FloatField(null=True, blank=True, verbose_name='<0.063 mm [%]')
    percent_finer_0_031mm = models.FloatField(null=True, blank=True, verbose_name='<0.031 mm [%]')

    def __str__(self):
        object_descrip = "{}".format(self.sample_id)
        return object_descrip


class IDO(models.Model):
    meas_station = models.ForeignKey(MeasStation, verbose_name='Measurement station', on_delete=models.SET_NULL,
                                     null=True,
                                     help_text='This field will be used to link the parametrical data tables'
                                               'to a given measurement point.')
    sample_id = models.CharField(max_length=200, help_text='This field is used to differentiate between duplicate '
                                                           'measurements performed in the same station. Thus, use the'
                                                           'same sample_id when it is intended to link'
                                                           'both IDO and kf profiles to one specific measurement'
                                                           'repetition.')
    dp_position = models.IntegerField(verbose_name='DP Position [-]',
                                      help_text='Double Packer Position. Mandatory field. Use intengers only.',
                                      null=True)
    sediment_depth_m = models.FloatField(null=True, verbose_name='Riverbed Depth [m]')
    idoc_mgl = models.FloatField(null=True, blank=True, verbose_name='IDOC [mg/l]', )
    temp_c = models.FloatField(null=True, blank=True, verbose_name='Temperature [°C]')
    idoc_sat = models.FloatField(null=True, blank=True, verbose_name='IDOS [%]')
    H_m = models.FloatField(null=True, blank=True, verbose_name='Height of filter pipe (Slurping) above bed [m]')
    operator_name = models.CharField(null=True, blank=True, max_length=100)
    comment = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.sample_id


class Kf(models.Model):
    # many-to-one relationship (many Kfs to one MeasStation)
    meas_station = models.ForeignKey(MeasStation, on_delete=models.SET_NULL, null=True,
                                     help_text='This field will be used to link the parametrical data tables'
                                               'to a given measurement point.'
                                     )
    sample_id = models.CharField(max_length=200, help_text='This field is used to differentiate between duplicate '
                                                           'measurements performed in the same station. Thus, use the'
                                                           'same sample_id when it is intended to link'
                                                           'both IDO and kf profiles to one specific measurement'
                                                           'repetition.')
    dp_position = models.IntegerField(verbose_name='DP Position [-]',
                                      help_text='Double Packer Position. Mandatory field. Use intengers only.',
                                      default=int,
                                      null=True)
    sediment_depth_m = models.FloatField(null=True, verbose_name='Riverbed depth [m]')
    kf_ms = models.FloatField(null=True, blank=True, verbose_name='kf [m/s]')
    slurp_rate_avg_mls = models.FloatField(null=True, blank=True, verbose_name='Slurping rate [mg/L]')
    H_m = models.FloatField(null=True, blank=True, verbose_name='Height of filter pipe (Slurping) above bed [m]')
    operator_name = models.CharField(null=True, blank=True, max_length=100)
    comment = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.sample_id


class Hydraulics(models.Model):
    SHIP = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('BLANK', 'Blank'),
    )
    # many-to-one relationship (many Hydraulics to one MeasStation)
    meas_station = models.ForeignKey(MeasStation, on_delete=models.SET_NULL, null=True)
    sample_id = models.CharField(max_length=200)
    v_x_ms = models.FloatField(null=True, blank=True, verbose_name='v_x [m/s]')
    v_y_ms = models.FloatField(null=True, blank=True, verbose_name='v_y [m/s]')
    v_z_ms = models.FloatField(null=True, blank=True, verbose_name='v_z [m/s]')
    kt = models.FloatField(null=True, blank=True, verbose_name='kt/U² [-]')
    kt_2d = models.FloatField(null=True, blank=True, verbose_name='kt 2d/U² [-]')
    v_bulk = models.FloatField(null=True, blank=True, verbose_name='U bulk [m/s]')
    water_temperature = models.FloatField(null=True, blank=True, verbose_name='Water temperature [°C]')
    turbidity_ntu = models.FloatField(null=True, blank=True, verbose_name='Turbidity [NTU]')
    operator_name = models.CharField(null=True, blank=True, max_length=100)
    ship_influence = models.CharField(null=True, max_length=100, choices=SHIP, blank=True)
