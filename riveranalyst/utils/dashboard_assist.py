import numpy as np
import plotly.express as px
from django_pandas.io import read_frame
from sklearn.decomposition import PCA
from riveranalyst.models import *
import plotly.io as pio


def get_corr_fig():
    """
    Function to collect database objects and perform spearman correlation analysis.
    :return: Plotly Figure, Dataframe
    """
    # get object from data models
    models = [Hydraulics, SubsurfaceSed, IDO, Kf, MeasStation]
    suffixes = {SubsurfaceSed: 'subsurf', Hydraulics: 'hyd'}
    objects_list = []
    for m in models:
        objects_list.append(m.objects.all())

    # creates df from filtered table
    vectorized_readdfs = np.vectorize(lambda x: read_frame(x))
    dfs = vectorized_readdfs(objects_list)

    # merge IDO table with Kf table
    df_global = dfs[-3].merge(dfs[-2], on=['meas_station', 'sample_id', 'dp_position'], how='outer')
    df_global = df_global.drop_duplicates(subset=['sample_id', 'dp_position'])

    # Average along the depth the IDO and Kf depth-profile value
    df_avg_ido_kf = df_global.groupby('meas_station', as_index=False).mean()

    # merge the depth-explicit dataframe with the stations table
    df_global = dfs[-1].merge(df_global, left_on='name', right_on='meas_station')

    # merge the average dataframe with the stations table
    df_global_avg = dfs[-1].merge(df_avg_ido_kf, left_on='name', right_on='meas_station')

    for i, df in enumerate(dfs[0:-3]):
        df_global = df_global.merge(df, on='meas_station',
                                    how='outer',
                                    suffixes=('', '_{}'.format(suffixes[models[i]])))
        df_global_avg = df_global_avg.merge(df, on='meas_station',
                                            how='outer',
                                            suffixes=('', '_{}'.format(suffixes[models[i]])))

    # correlation
    takeoff_cols = ['id_surf', 'id_subsurf', 'id_x', 'id_y', 'id', 'x', 'y', 'x_epsg', 'y_epsg',
                    'x_epsg4326', 'y_epsg4326', 'sediment_depth_m_x', 'comment_x', 'comment_y',
                    'dp_position', 'sediment_depth_m_y', ]
    df_final = df_global.loc[:, ~df_global.columns.isin(takeoff_cols)]
    df_corr = df_final.corr(method='spearman').round(1)

    depth_explicit_feats = ['kf_ms', 'slurp_rate_avg_mls',
                            'idoc_mgl', 'idoc_sat', 'temp_c']

    # Correlation matrix just between bulk parameters
    fig = px.imshow(df_corr.loc[depth_explicit_feats, :], text_auto=True, aspect='auto')
    return fig, df_global_avg


def get_PCA(df):
    # Preparing df for dimensinality reduction
    features = ['idoc_mgl', 'wl_m', 'slurp_rate_avg_mls', 'river',
                'd84', 'dm', 'geom_std_grain',
                'percent_finer_2mm',
                'percent_finer_0_5mm',
                'name'
                ]

    df4pca = df[features].dropna()

    df4pca_prescaling = df4pca.drop(['river', 'name'], axis=1)

    # Scaling with s-score apporach
    df4pca_final = df4pca_prescaling.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

    # Build PCA
    pca = PCA(n_components=4)
    components = pca.fit_transform(df4pca_final)
    variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(variance)
    total_var2d = variance.sum() * 100

    # Get labels for explaind variance respective tot he PC
    labels = {
        str(i): f"PC {i + 1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    # Plot data 2-dimensionaly in the new coordinate system of PCs
    fig2d = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(4),
        color=df4pca["river"],
        symbol=df4pca['river'],
        title=f'Total Explained Variance: {total_var2d:.2f}%',
        color_discrete_sequence=px.colors.qualitative.Bold,
        width=1000, height=700,
        hover_name=df4pca['name'],
    )
    fig2d.update_traces(diagonal_visible=False)
    # Set the desired width, height, and scale values
    pio.write_image(fig2d, 'pca_matrix.png', scale=4)

    # Plot data 3-dimensionaly in the new coordinate system of PCs
    total_var = pca.explained_variance_ratio_.sum() * 100
    fig3d = px.scatter_3d(
        components, x=0, y=1, z=2, color=df4pca['river'],
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # Visualizing loadings of each components
    # pca2d = PCA(n_components=2)
    components2d = pca.fit_transform(df4pca_final)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    np.savetxt('loadings.csv', loadings, delimiter=',')

    fig_load = px.scatter(components2d, x=0, y=1, color=df4pca['river'], symbol=df4pca['river'],
                          range_color=[-1000, 1000],
                          width=1000, height=600,
                          labels={'0': 'PC 1', '1': 'PC 2'},
                          title='Loadings',
                          color_discrete_sequence=px.colors.qualitative.Bold, )
    feat_annotation = ['IDOC', 'Water depth', 'Slurping rate', 'River',
                        'd84', 'dm', 'sigma_g',
                        'FSF < 2 mm',
                        'FSF < 0.5 mm'
                ]
    annotate_dict = {features[i]: feat_annotation[i] for i in range(len(feat_annotation))}
    for i, feature in enumerate(df4pca_final.columns):
        fig_load.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=loadings[i, 0] * 4,
            y=loadings[i, 1] * 4,
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top"
        )
        fig_load.add_annotation(
            x=loadings[i, 0] * 4,
            y=loadings[i, 1] * 4,
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=annotate_dict[feature],
            yshift=5,
        )

    return fig2d, fig3d, fig_load

