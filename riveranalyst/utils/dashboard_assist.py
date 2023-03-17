import pandas as pd
import numpy as np
import plotly.express as px
from django_pandas.io import read_frame
from riveranalyst.models import *


def get_corr_fig():
    # get object from data models
    models = [Hydraulics, SubsurfaceSed, SurfaceSed, IDO, Kf, MeasStation]
    suffixes = {SubsurfaceSed: 'subsurf', SurfaceSed: 'surf', Hydraulics: 'hyd'}
    objects_list = []
    for m in models:
        objects_list.append(m.objects.all())

    # creates df from filtered table
    vectorized_readdfs = np.vectorize(lambda x: read_frame(x))
    dfs = vectorized_readdfs(objects_list)

    df_global = dfs[-3].merge(dfs[-2], on=['meas_station', 'sample_id', 'dp_position'], how='outer')
    df_global = df_global.drop_duplicates(subset=['sample_id', 'dp_position'])

    df_global = dfs[-1].merge(df_global, left_on='name', right_on='meas_station')
    df_global.to_csv('save_intermed.csv')
    for i, df in enumerate(dfs[0:-3]):
        # df2include = df[[c for c in list(df.columns) if c != 'meas_station']]
        # df2include = df2include.add_suffix('_{}'.format(suffixes[models[i+1]]))
        df_global = df_global.merge(df, on='meas_station',
                                    how='outer',
                                    suffixes=('', '_{}'.format(suffixes[models[i]])))

    df_global.to_csv('save_finalmaybe.csv')

    # correlation
    takeoff_cols = ['id_surf', 'id_subsurf', 'id_x', 'id_y', 'id', 'x', 'y', 'x_epsg', 'y_epsg', 'x_epsg4326', 'y_epsg4326']
    df_corr = df_global.loc[:, ~df_global.columns.isin(takeoff_cols)].corr().round(1)

    # mask to matrix
    mask = np.zeros_like(df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    # viz
    df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna('columns', how='all')
    fig = px.imshow(df_corr_viz, text_auto=True)
    return fig