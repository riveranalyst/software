import pandas as pd
import numpy as np
import plotly.express as px
from django_pandas.io import read_frame
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
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
    df_final = df_global.loc[:, ~df_global.columns.isin(takeoff_cols)]
    df_corr = df_final.corr().round(1)

    # mask to matrix
    mask = np.zeros_like(df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    # viz
    df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna('columns', how='all')
    fig = px.imshow(df_corr_viz, text_auto=True, width=1000, height=1000)
    return fig, df_final


def get_PCA(df):
    # Preparing df for dimensinality reduction
    features = ['idoc_mgl', 'wl_m', 'kf_ms', 'temp_c', 'river',
                'n_wooster', 'd10', 'd50', 'd90', 'so', 'dm', 'dg',
                'percent_finer_2mm', 'percent_finer_1mm', 'percent_finer_0_5mm']
    df4pca = df[features].dropna()
    df4pca_prescaling = df4pca.drop(['river'], axis=1)

    # Scaling with s-score apporach
    df4pca_final = df4pca_prescaling.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

    # Build PCA
    pca = PCA(n_components=4)
    components = pca.fit_transform(df4pca_final)

    # Get labels for explaind variance respective tot he PC
    labels = {
        str(i): f"PC {i + 1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }
    total_var2d = pca.explained_variance_ratio_.sum() * 100

    # Plot data 2-dimensionaly in the new coordinate system of PCs
    fig2d = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(4),
        color=df4pca["river"],
        title=f'Total Explained Variance: {total_var2d:.2f}%',
        width=1000, height=600,
    )
    fig2d.update_traces(diagonal_visible=False)

    # Plot data 3-dimensionaly in the new coordinate system of PCs
    pca3d = PCA(n_components=3)
    components3d = pca3d.fit_transform(df4pca_final)
    total_var = pca3d.explained_variance_ratio_.sum() * 100
    fig3d = px.scatter_3d(
        components3d, x=0, y=1, z=2, color=df4pca['river'],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
    )

    # Visualizing loadings of each components
    loadings = pca3d.components_.T * np.sqrt(pca3d.explained_variance_)
    fig_load = px.scatter(components3d, x=0, y=1, color=df4pca['river'], width=1000, height=600,
                          labels={'0': 'PC 1', '1': 'PC 2'})
    for i, feature in enumerate(df4pca_final.columns):
        fig_load.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=loadings[i, 0]*4,
            y=loadings[i, 1]*4,
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top"
        )
        fig_load.add_annotation(
            x=loadings[i, 0]*4,
            y=loadings[i, 1]*4,
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5,
        )
    return fig2d, fig3d, fig_load
