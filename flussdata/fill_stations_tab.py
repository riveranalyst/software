import os
import django
from pathlib import Path
import numpy as np
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
        # coll_data, created = models.CollectedData.objects.get_or_create(collected_data=row.collected_data)
        st = models.MeasStation.objects.create(
            name=row.meas_station.strip(),
            river=ri,
            campaign=ca,
            date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
            description=row.description,
            # collected_data=coll_data,
            lon=row.lon,
            lat=row.lat,
            pos_rel_WB=row.pos_rel_WB_m,
            discharge=row.dis_cumec,
            wl_m=row.wl_m,
            wl_model_m=row.wl_model_m,
            algae_cover=row.algae_cover,
            imbrication=row.imbrication,
            bed_slope=row.bed_slope,
        )
        st.save()


if __name__ == '__main__':
    # filling initial data
    # column_dtypes = {'imbrication': "boolean",
    #                  'algae_cover': "boolean"}
    st_df = pd.read_excel(BASE_DIR / 'media/db-baseline-stations.xlsx',
                          engine='openpyxl')
    fill_st_model(st_df)