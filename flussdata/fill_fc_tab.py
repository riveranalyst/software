import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent


# fill database with the table just read preivously
def fill_fc_model(df):
    for index, row in df.iterrows():
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # get the sampling technique from the Sampling Class
        samp_method = models.SedSamplTechnique.objects.get(
            samp_techniques=row.sampling_method.strip()
        )

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(models.CollectedData.objects.get(collected_data='SubsurfSed'))

        # Create new sediment sample observation (row) from the input table
        new_freezecore, created = models.SubsurfaceSed.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            sampling_method=samp_method,
            porosity_sfm=row.porosity_sfm,
            dm=row.dm,
            dg=row.dg,
            fi=row.fi,
            geom_std_grain=row.geom_std_grain,
            d10=row.d10,
            d16=row.d16,
            d25=row.d25,
            d30=row.d30,
            d50=row.d50,
            d60=row.d60,
            d75=row.d75,
            d84=row.d84,
            d90=row.d90,
            cu=row.cu,
            cc=row.cc,
            fsf_le_2mm=row.fsf_le_2mm,
            fsf_le_1mm=row.fsf_le_1mm,
            fsf_le_0_5mm=row.fsf_le_0_5mm,
            so=row.so,
            wl_slurp_m=row.wl_slurp_m,
            wl_model_m=row.wl_model_m,
            n_wooster=row.n_wooster,
            bed_slope=row.bed_slope,
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
            percent_finer_0_031mm=row.percent_finer_0_031mm)
        new_freezecore.save()


if __name__ == '__main__':
    # filling initial data
    freezecore_df = pd.read_excel(BASE_DIR / 'media/db-baseline-FC.xlsx', engine='openpyxl')
    fill_fc_model(freezecore_df)
