import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent


# fill database with the table just read preivously
def fill_idoc_model(df):
    for index, row in df.iterrows():
        ri, created = models.River.objects.get_or_create(river=row.river.strip())
        ca, created = models.Campaign.objects.get_or_create(campaign=row.campaign)

        # is tht station already exist, then get it and add a method tag
        if models.MeasStation.objects.filter(name=row.meas_station.strip()).exists():
            #print('entered the if')
            st = models.MeasStation.objects.get(name=row.meas_station.strip())
            #print(st)
            st.method.add(models.Technique.objects.get(method='IDOC'))
            #st.method.add(models.Technique.objects.get(method='FC'))
        # if station of the IDOC doesnt match with anything then create it
        else:
            st = models.MeasStation(
                river=ri,
                campaign=ca,
                # method=,
                name=row.meas_station.strip(),
                date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
                #description=''
            )
            st.save()
            st.method.add(models.Technique.objects.get(method='IDOC'))

        new_vertico = models.IDOC(
            meas_station=st,
            sample_id=row.sample_id,
            # site_name=row.site_name,
            # date=row.date,
            lon=row.lon,
            lat=row.lat,
            dp_position=row.dp_position,
            sediment_depth_m=row.sediment_depth_m,
            wl_m=row.wl_m,
            H_m=row.H_m,
            # slurp_rate_avg_mls=row.slurp_rate_avg_mls,
            idoc_mgl=row.idoc_mgl,
            temp_c=row.temp_c,
            idoc_sat=row.idoc_sat,
            # kf_ms=row.kf_ms,
            comment=row.comment)
        new_vertico.save()


if __name__ == '__main__':
    idoc_df = pd.read_excel(BASE_DIR / 'media/db-baseline-idoc.xlsx', engine='openpyxl')
    fill_idoc_model(idoc_df)