import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import pandas as pd
import flussdata.models as models

BASE_DIR = Path(__file__).resolve().parent.parent

# filling initial data
freezecore_df = pd.read_excel(BASE_DIR / 'media/db-baseline-FC.xlsx', engine='openpyxl')

# fill database with the table just read preivously
for index, row in freezecore_df.iterrows():
    new_freezecore_df = models.Freezecore(
        river=row.river,
        sample_id=row.sample_id,
        sample_name=row.sample_name,
        site_name=row.site_name,
        date=row.date,
        time_stamp=row.time_stamp,
        lon=row.lon,
        lat=row.lat,
        porosity_sfm=row.porosity_sfm,
        dm=row.dm,
        dg=row.dg,
        fi=row.fi,
        geom_std_grain=row.geom_std_grain,
        d10=row.d10,
        d16=row.d16,
        d25=row.d25,
        d30=row.d30,
        d50=row.d50,
        d60=row.d60,
        d75=row.d75,
        d84=row.d84,
        d90=row.d90,
        cu=row.cu,
        cc=row.cc,
        fsf_le_2mm=row.fsf_le_2mm,
        fsf_le_1mm=row.fsf_le_1mm,
        fsf_le_0_5mm=row.fsf_le_0_5mm,
        so=row.so,
        wl_slurp_m=row.wl_slurp_m,
        wl_model_m=row.wl_model_m,
        n_wooster=row.n_wooster,
        bed_slope=row.bed_slope,
        comment=row.comment,
        percent_finer_250mm=row.percent_finer_250mm,
        percent_finer_125mm=row.percent_finer_125mm,
        percent_finer_63mm=row.percent_finer_63mm,
        percent_finer_31_5mm=row.percent_finer_31_5mm,
        percent_finer_16mm=row.percent_finer_16mm,
        percent_finer_8mm=row.percent_finer_8mm,
        percent_finer_4mm=row.percent_finer_4mm,
        percent_finer_2mm=row.percent_finer_2mm,
        percent_finer_1mm=row.percent_finer_1mm,
        percent_finer_0_5mm=row.percent_finer_0_5mm,
        percent_finer_0_25mm=row.percent_finer_0_25mm,
        percent_finer_0_125mm=row.percent_finer_0_125mm,
        percent_finer_0_063mm=row.percent_finer_0_063mm,
        percent_finer_0_031mm=row.percent_finer_0_031mm)
    new_freezecore_df.save()

