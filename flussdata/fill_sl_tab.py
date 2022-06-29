import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent

idoc_df = pd.read_excel(BASE_DIR/'media/db-baseline-idoc.xlsx', engine='openpyxl')


#TODO
# Use River. Campaign. and MeasStation.get_or_create() to initialize tables

# loops through all unique values of the column river and create a River object
# in case it is not contained already in the model/table
for river in idoc_df['river'].unique():
    print(river)
    if not models.River.objects.filter(river=river).exists():
        new_river = models.River(river=river)
        new_river.save()

# same but now for the column campaign
for campaign in idoc_df['campaign'].unique():
    if not models.Campaign.objects.filter(campaign=campaign).exists():
        new_campaign = models.Campaign(campaign=campaign)
        new_campaign.save()

# same but now for the meas_station
for index, row in idoc_df.drop_duplicates(subset=['meas_station']).iterrows():
    if not models.MeasStation.objects.filter(name=row.meas_station).exists():
        new_measstation = models.MeasStation(
            river=models.River.objects.get(river=row.river),
            campaign=models.Campaign.objects.get(campaign=row.campaign),
            method='FC',
            name=row.meas_station,
            date=row.date,  # 'date of measureemnt' is the verbose name (optional arg)
            description=''
        )
        new_measstation.save()


# fill database with the table just read preivously
for index, row in idoc_df.iterrows():
    new_vertico_model = models.IDOC(
        meas_station=models.MeasStation.objects.get(name=row.meas_station),
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
    new_vertico_model.save()
