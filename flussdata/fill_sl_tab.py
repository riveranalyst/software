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
def fill_idoc_model(df):
    for index, row in df.iterrows():
        # get each station object from Station Class
        st = models.MeasStation.objects.get(
            name=row.meas_station.strip(),
        )

        # Fill information about water levels if it wasn't available before
        if st.wl_m is None:
            st.wl_m = row.wl_m
        if st.H_m is None:
            st.H_m = row.H_m
        st.save()

        # Add information to the station that data is avaialble for idoc
        st.collected_data.add(models.CollectedData.objects.get(collected_data='IDOC'))

        # Create new idoc observation (row) from the input table
        idoc, created = models.IDOC.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            dp_position=row.dp_position,
            sediment_depth_m=row.sediment_depth_m,
            idoc_mgl=row.idoc_mgl,
            temp_c=row.temp_c,
            idoc_sat=row.idoc_sat,
            comment=row.comment)
        idoc.save()


if __name__ == '__main__':
    idoc_df = pd.read_excel(BASE_DIR / 'media/db-baseline-idoc.xlsx', engine='openpyxl')
    fill_idoc_model(idoc_df)