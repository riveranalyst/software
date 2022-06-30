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
        ri, created = models.River.objects.get_or_create(river=row.river.strip())
        ca, created = models.Campaign.objects.get_or_create(campaign=row.campaign)
        # me, created =
        st, created = models.MeasStation.objects.get_or_create(
            river=ri,
            campaign=ca,
            #method=models.Technique.objects.get(method='FC'),
            name=row.meas_station.strip(),
            date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
            #description=''
        )
        st.method.add(models.Technique.objects.get(method='FC'))
        #st.save()
        new_freezecore = models.Freezecore(
            meas_station=st,
            sample_id=row.sample_id,
            sample_name=row.sample_name,
            site_name=row.site_name,
            lon=row.lon,
            lat=row.lat,
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
