import os
import django
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
# necessary to find file within the project dir
BASE_DIR = Path(__file__).resolve().parent.parent
import riveranalyst.models as models
from django_pandas.io import read_frame


st_objects = models.MeasStation.objects.all()
ido_objects = models.IDO.objects.all()
kf_objects = models.Kf.objects.all()

ido_df = read_frame(ido_objects)
st_df = read_frame(st_objects)
kf_df = read_frame(kf_objects)

# option how=outer is to ensure the union instead of intersection of the two dfs
kf_idoc = ido_df.merge(kf_df, on=['sample_id', 'dp_position'], how='outer')
kf_idoc = kf_idoc.drop_duplicates(subset=['sample_id', 'dp_position'])

kf_idoc_st = st_df.merge(ido_df, left_on='name', right_on='meas_station')
kf_idoc_st.to_csv('merge-kf-idoc-st.csv')