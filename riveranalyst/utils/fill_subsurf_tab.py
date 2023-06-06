import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import riveranalyst.models as models
import numpy as np


# fill database with the table just read preivously
def fill_subsurf_model(df):
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        print(row.meas_station)
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


if __name__ == '__main__':
    # Reset the data model SubsurfaceSed
    models.SubsurfaceSed.objects.all().delete()

    # necessary to find file within the project dir
    BASE_DIR = Path(__file__).resolve().parent.parent

    # filling initial data
    freezecore_df = pd.read_excel(BASE_DIR / 'media/db-baseline-subsurf.xlsx', engine='openpyxl')
    fill_subsurf_model(freezecore_df)
