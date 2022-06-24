import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent

vertico_df = pd.read_excel(BASE_DIR/'media/db-baseline-SL.xlsx', engine='openpyxl')

# fill database with the table just read preivously
for index, row in vertico_df.iterrows():
    new_vertico_model = models.VertiCo(
        river=row.river,
        sample_id=row.sample_id,
        sample_name=row.sample_name,
        site_name=row.site_name,
        date=row.date,
        time_stamp=row.time_stamp,
        lon=row.lon,
        lat=row.lat,
        dp_position=row.dp_position,
        sediment_depth_m=row.sediment_depth_m,
        wl_m=row.wl_m,
        H_m=row.H_m,
        slurp_rate_avg_mls=row.slurp_rate_avg_mls,
        idoc_mgl=row.idoc_mgl,
        temp_c=row.temp_c,
        idoc_sat=row.idoc_sat,
        kf_ms=row.kf_ms,
        comment=row.comment)
    new_vertico_model.save()
