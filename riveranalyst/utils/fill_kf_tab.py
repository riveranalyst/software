import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
import pandas as pd
import riveranalyst.models as models
import numpy as np

# necessary to find file within the project dir
BASE_DIR = Path(__file__).resolve().parent.parent


# fill database with the table template
def fill_kf_model(df):
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

        # get or create the data class and add it to the stations information
        data_station = models.CollectedData.objects
        data_type, created = data_station.get_or_create(collected_data='kf')

        # Add information to the station that data is avaialble for subsurface sediments
        st.collected_data.add(data_type)

        # Create new idoc observation (row) from the input table
        kf, created = models.Kf.objects.get_or_create(
            meas_station=st,
            sample_id=row.sample_id,
            dp_position=row.dp_position,
            sediment_depth_m=row.sediment_depth_m,
            kf_ms=row.kf_ms,
            slurp_rate_avg_mls=row.slurp_rate_avg_mls,
            operator_name=row.operator_name,
            H_m=row.H_m,
            comment=row.comment)
        kf.save()


if __name__ == '__main__':
    # Reset the data model Kf
    models.Kf.objects.all().delete()

    kf_df = pd.read_excel(BASE_DIR / 'media/db-baseline-kf.xlsx', engine='openpyxl')
    fill_kf_model(kf_df)
