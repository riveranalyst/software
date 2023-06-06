import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import riveranalyst.models as models
from pyproj import transform, CRS, Proj, exceptions
import numpy as np


# fill database with the table just read preivously
def fill_st_model(df):
    df = df.replace({np.nan: None})
    outproj_str = 'epsg:4326'
    proj_4326 = CRS.from_string(outproj_str)
    for index, row in df.iterrows():
        ri, created = models.River.objects.get_or_create(river=row.river.strip())
        ca, created = models.Survey.objects.get_or_create(survey=row.survey)

        try:
            # check for coord system and if necessary reproject coords to epsg4326
            if row.coord_system == outproj_str:
                y_epsg4326 = row.y
                x_epsg4326 = row.x
            # for gauss kruger, the easting and northing are inversed, see eg.: https://epsg.io/31468
            eastnorth_insteadof_northeast_projs = ['epsg:31468', 'epsg:5684', 'epsg:32632', 'epsg:3857', 'epsg:25832']
            if row.coord_system in eastnorth_insteadof_northeast_projs:
                y_epsg4326, x_epsg4326 = transform(
                    CRS.from_string(row.coord_system), proj_4326, row.x, row.y)
            else:
                x_epsg4326, y_epsg4326 = transform(
                    CRS.from_string(row.coord_system), proj_4326, row.x, row.y)
        except (exceptions.CRSError, TypeError) as e:
            print(row.meas_station)
            print(e)
            y_epsg4326 = np.nan
            x_epsg4326 = np.nan
            pass
        # coll_data, created = models.CollectedData.objects.get_or_create(collected_data=row.collected_data)
        # print(row.meas_station)
        st = models.MeasStation.objects.create(
            name=row.meas_station.strip(),
            river=ri,
            survey=ca,
            date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
            description=row.description,
            x=row.x,
            y=row.y,
            y_epsg4326=y_epsg4326,
            x_epsg4326=x_epsg4326,
            coord_system=row.coord_system,
            bed_elevation_wgs84=row.bed_elevation_wgs84,
            bed_elevation_dhhn=row.bed_elevation_dhhn,
            pos_rel_WB=row.pos_rel_WB_m,
            discharge=row.dis_cumec,
            wl_m=row.wl_m,
            wl_model_m=row.wl_model_m,
            algae_cover=row.algae_cover,
            imbrication=row.imbrication,
            bed_slope=row.bed_slope,
        )
        st.save()


# fill database with the table template
def fill_do_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # Fill information about water levels if it wasn't available before
        if st.wl_m is None:
            st.wl_m = row.wl_m
        st.save()
        # print(row.meas_station)
        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='IDO')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new idoc observation (row) from the input table
        idoc, created = models.IDO.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            dp_position=row.dp_position,
            sediment_depth_m=row.sediment_depth_m,
            idoc_mgl=row.idoc_mgl,
            temp_c=row.temp_c,
            idoc_sat=row.idoc_sat,
            operator_name=row.operator_name,
            H_m=row.H_m,
            comment=row.comment)
        idoc.save()


# fill database with the table template
def fill_kf_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # Fill information about water levels if it wasn't available before
        if st.wl_m is None:
            st.wl_m = row.wl_m
        st.save()

        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='kf')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new idoc observation (row) from the input table
        kf, created = models.Kf.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            dp_position=row.dp_position,
            sediment_depth_m=row.sediment_depth_m,
            kf_ms=row.kf_ms,
            slurp_rate_avg_mls=row.slurp_rate_avg_mls,
            operator_name=row.operator_name,
            H_m=row.H_m,
            comment=row.comment)
        kf.save()


# fill database with the table just read preivously
def fill_subsurf_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # print(row.meas_station)
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # get the sampling technique from the Sampling Class
        samp_method, created = models.SedSamplTechnique.objects.get_or_create(
            samp_techniques=row.sampling_method.strip()
        )

        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='SubsurfSed')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new sediment sample observation (row) from the input table
        new_freezecore, created = models.SubsurfaceSed.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            sampling_method=samp_method,
            operator_name=row.operator_name,

            # Actual variables
            dm=row.dm,
            dg=row.dg,
            fi=row.fi,
            std_grain=row.std_grain,
            geom_std_grain=row.geom_std_grain,
            skewness=row.skewness,
            kurtosis=row['kurtosis'],  # necessary since pandas has a method called 'kurtosis' too
            cu=row.cu,
            cc=row.cc,
            n_carling=row.n_carling,
            n_wu_wang=row.n_wu_wang,
            n_wooster=row.n_wooster,
            n_frings=row.n_frings,
            n_user=row.n_user,
            d10=row.d10,
            d16=row.d16,
            d25=row.d25,
            d30=row.d30,
            d50=row.d50,
            d60=row.d60,
            d75=row.d75,
            d84=row.d84,
            d90=row.d90,
            so=row.so,
            comment=row.comment,
            percent_finer_250mm=row.percent_finer_250mm,
            percent_finer_125mm=row.percent_finer_125mm,
            percent_finer_63mm=row.percent_finer_63mm,
            percent_finer_31_5mm=row.percent_finer_31_5mm,
            percent_finer_16mm=row.percent_finer_16mm,
            percent_finer_8mm=row.percent_finer_8mm,
            percent_finer_4mm=row.percent_finer_4mm,
            percent_finer_2mm=row.percent_finer_2mm,
            percent_finer_1mm=row.percent_finer_1mm,
            percent_finer_0_5mm=row.percent_finer_0_5mm,
            percent_finer_0_25mm=row.percent_finer_0_25mm,
            percent_finer_0_125mm=row.percent_finer_0_125mm,
            percent_finer_0_063mm=row.percent_finer_0_063mm,
            percent_finer_0_031mm=row.percent_finer_0_031mm, )
        new_freezecore.save()


# fill database with the table just read preivously
def fill_surf_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # print(row.meas_station)
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # get the sampling technique from the Sampling Class
        samp_method, created = models.SedSamplTechnique.objects.get_or_create(
            samp_techniques=row.sampling_method.strip()
        )

        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='SurfSed')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new sediment sample observation (row) from the input table
        new_sample, created = models.SurfaceSed.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            sampling_method=samp_method,
            operator_name=row.operator_name,

            # Actual variables
            dm=row.dm,
            dg=row.dg,
            fi=row.fi,
            std_grain=row.std_grain,
            geom_std_grain=row.geom_std_grain,
            skewness=row.skewness,
            kurtosis=row['kurtosis'],  # necessary since pandas has a method called 'kurtosis' too
            cu=row.cu,
            cc=row.cc,
            n_carling=row.n_carling,
            n_wu_wang=row.n_wu_wang,
            n_wooster=row.n_wooster,
            n_frings=row.n_frings,
            d10=row.d10,
            d16=row.d16,
            d25=row.d25,
            d30=row.d30,
            d50=row.d50,
            d60=row.d60,
            d75=row.d75,
            d84=row.d84,
            d90=row.d90,
            so=row.so,
            comment=row.comment,
            percent_finer_250mm=row.percent_finer_250mm,
            percent_finer_125mm=row.percent_finer_125mm,
            percent_finer_63mm=row.percent_finer_63mm,
            percent_finer_31_5mm=row.percent_finer_31_5mm,
            percent_finer_16mm=row.percent_finer_16mm,
            percent_finer_8mm=row.percent_finer_8mm,
            percent_finer_4mm=row.percent_finer_4mm,
            percent_finer_2mm=row.percent_finer_2mm,
            percent_finer_1mm=row.percent_finer_1mm,
            percent_finer_0_5mm=row.percent_finer_0_5mm,
            percent_finer_0_25mm=row.percent_finer_0_25mm,
            percent_finer_0_125mm=row.percent_finer_0_125mm,
            percent_finer_0_063mm=row.percent_finer_0_063mm,
            percent_finer_0_031mm=row.percent_finer_0_031mm, )
        new_sample.save()


# fill database with the table template
def fill_hydraulics_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='Hydraulics')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new idoc observation (row) from the input table
        hydraulics, created = models.Hydraulics.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            v_x_ms=row.v_x_ms,
            v_y_ms=row.v_y_ms,
            v_z_ms=row.v_z_ms,
            kt=row.kt,
            kt_2d=row.kt_2d,
            v_bulk=row.v_bulk,
            water_temperature=row.water_temperature,
            operator_name=row.operator_name,
            ship_influence=row.ship_influence,
        )
        hydraulics.save()