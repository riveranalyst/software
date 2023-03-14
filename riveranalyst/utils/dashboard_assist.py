import pandas as pd
import riveranalyst.models as models
import numpy as np
import plotly.express as px
from django_pandas.io import read_frame
from riveranalyst.models import *


def get_corr_fig():
    models = [SubsurfaceSed, SurfaceSed, IDO, MeasStation, Kf, Hydraulics]
    objects_list = []
    for m in models:
        objects_list.append(m.objects.all())
    # subsurf_objects = SubsurfaceSed.objects.all()
    # surf_objects = SurfaceSed.objects.all()
    # idoc_objects = IDO.objects.all()
    # station_objects = MeasStation.objects.all()
    # kf_objects = Kf.objects.all()
    # v_objects = Hydraulics.objects.all()

    # creates df from filtered table
    vectorized_readdfs = np.vectorize(lambda x: read_frame(x))
    dfs = vectorized_readdfs(objects_list)
    df_global = pd.concat(dfs)

    # Correlation
    df_corr = df_global.corr().round(1)
    # Mask to matrix
    mask = np.zeros_like(df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    # Viz
    df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna('columns', how='all')
    fig = px.imshow(df_corr_viz, text_auto=True)
    return fig