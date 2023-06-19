from riveranalyst.utils.fill_funcs import *
from django.apps import apps
from pathlib import Path
import pandas as pd
import time

BASE_DIR = Path(__file__).resolve().parent.parent

model_names = ['MeasPosition', 'IDO', 'Kf', 'SubsurfaceSed', 'SurfaceSed', 'Hydraulics']
table_paths = [BASE_DIR / 'media/db-baseline-positions.xlsx',
               BASE_DIR / 'media/db-baseline-idoc.xlsx',
               BASE_DIR / 'media/db-baseline-kf.xlsx',
               BASE_DIR / 'media/db-baseline-subsurf.xlsx',
               BASE_DIR / 'media/db-baseline-surf.xlsx',
               BASE_DIR / 'media/db-baseline-hydraulics.xlsx'
               ]

dict = dict(zip(model_names, table_paths))

func_list = [fill_measpositions_model,
             fill_do_model,
             fill_kf_model,
             fill_subsurf_model,
             fill_surf_model,
             fill_hydraulics_model]

start_time = time.time()


for model_name, table_path, fill_func in zip(model_names, table_paths, func_list):
    print('Populating the {} table...'.format(model_name))
    model = apps.get_model(app_label='riveranalyst', model_name=model_name)  # Replace 'your_app_label' with the appropriate app label
    model.objects.all().delete()
    df = pd.read_excel(table_path, engine='openpyxl')
    fill_func(df)

elapsed_time = time.time() - start_time

print('Time taken to populate database was {} seconds.'.format(elapsed_time))

