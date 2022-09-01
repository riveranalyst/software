import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models

# necessary to find file within the project dir
BASE_DIR = Path(__file__).resolve().parent.parent


# fill database with the table template
def fill_hydraulics_model(df):
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
            sample_id = row.sample_id,
            v_x = row.v_x,
            v_y = row.v_y,
            v_z = row.v_z,
            kt = row.kt,
            kt_2d = row.kt_2d,
            v_bulk=row.v_bulk,
            water_temperature = row.water_temperature,
            turbidity = row.turbidity,
            operator_name = row.operator_name,
            ship_influence = row.ship_influence,
        )
        hydraulics.save()


if __name__ == '__main__':
    hyd_df = pd.read_excel(BASE_DIR / 'media/db-baseline-hyd.xlsx', engine='openpyxl')
    fill_hydraulics_model(hyd_df)