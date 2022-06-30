import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent


# fill database with the table just read preivously
def fill_st_model(df):
    for index, row in df.iterrows():
        ri, created = models.River.objects.get_or_create(river=row.river.strip())
        ca, created = models.Campaign.objects.get_or_create(campaign=row.campaign)

        st, created = models.MeasStation.objects.get_or_create(
            river=ri,
            campaign=ca,
            name=row.meas_station.strip(),
            date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
            lon=row.lon,
            lat=row.lat,
            # description='',
            wl_m=row.wl_m,
            H_m=row.H_m
        )
        #st.method.add(models.Technique.objects.get(method='FC'))
        st.save()


if __name__ == '__main__':
    # filling initial data
    st_df = pd.read_excel(BASE_DIR / 'media/db-baseline-stations.xlsx', engine='openpyxl')
    fill_st_model(st_df)
