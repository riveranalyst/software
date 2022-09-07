import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import flussdata.models as models
import numpy as np
# necessary to find file within the project dir
BASE_DIR = Path(__file__).resolve().parent.parent


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


if __name__ == '__main__':
    models.IDO.objects.all().delete()
    idoc_df = pd.read_excel(BASE_DIR / 'media/db-baseline-idoc.xlsx', engine='openpyxl')
    fill_do_model(idoc_df)