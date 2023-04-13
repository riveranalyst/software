import numpy as np
import plotly.express as px
from django_pandas.io import read_frame
from sklearn.decomposition import PCA
from riveranalyst.models import *
import plotly.io as pio
import plotly.graph_objects as go


def get_corr_fig():
    # get object from data models
    models = [Hydraulics, SubsurfaceSed, IDO, Kf, MeasStation]
    suffixes = {SubsurfaceSed: 'subsurf', Hydraulics: 'hyd'}
    objects_list = []
    for m in models:
        objects_list.append(m.objects.all())

    # creates df from filtered table
    vectorized_readdfs = np.vectorize(lambda x: read_frame(x))
    dfs = vectorized_readdfs(objects_list)

    df_global = dfs[-3].merge(dfs[-2], on=['meas_station', 'sample_id', 'dp_position'], how='outer')
    df_global = df_global.drop_duplicates(subset=['sample_id', 'dp_position'])
    df_avg_ido_kf = df_global.groupby('meas_station', as_index=False).mean()
    # df_avg_ido_kf.to_csv('df_avg_ido_kf.csv')

    df_global = dfs[-1].merge(df_global, left_on='name', right_on='meas_station')
    df_global_avg = dfs[-1].merge(df_avg_ido_kf, left_on='name', right_on='meas_station')

    for i, df in enumerate(dfs[0:-3]):
        # df2include = df[[c for c in list(df.columns) if c != 'meas_station']]
        # df2include = df2include.add_suffix('_{}'.format(suffixes[models[i+1]]))
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

    # # Get number of samples per correlation value
    # df_get_ns = pd.DataFrame(index=df_corr.index, columns=df_corr.columns)
    #
    # for index_1 in df_get_ns.index:
    #     for index_2 in df_get_ns.index:
    #         df_get_dropped = df_final[[index_1, index_2]].dropna()
    #         count_n = df_get_dropped[index_1].dropna().count()
    #         df_get_ns.at[index_1, index_2] = count_n
    # print(df_get_ns)

    depth_explicit_feats = ['kf_ms', 'slurp_rate_avg_mls',
                            'idoc_mgl', 'idoc_sat', 'temp_c']

    # Correlation matrix just between bulk parameters
    # df_final_seds = df_final.loc[:, ~df_final.columns.isin(depth_explicit_feats)]
    # df_final_seds = df_final_seds.drop_duplicates()
    # df_final_seds.to_csv('drop_duplicates_for_corr_seds.csv')
    # df_corr_seds = df_final_seds.corr(method='spearman').round(1)
    # # mask to matrix
    # mask = np.zeros_like(df_corr_seds, dtype=bool)
    # mask[np.triu_indices_from(mask)] = True
    # viz
    # df_corr_seds_viz = df_corr_seds.mask(mask).dropna(how='all').dropna('columns', how='all')

    fig = px.imshow(df_corr.loc[depth_explicit_feats, :], text_auto=True, aspect='auto')
    # fig2 = px.imshow(df_corr_seds_viz, text_auto=True, aspect='auto')
    # df_global_avg.to_csv('df_global_avg.csv')
    return fig, df_global_avg


def get_PCA(df):
    # Preparing df for dimensinality reduction
    features = ['idoc_mgl', 'wl_m', 'kf_ms', 'river',
                'n_wooster', 'd10', 'd50', 'd90', 'so', 'dm', 'dg',
                'percent_finer_1mm']
    df4pca = df[features].dropna()
    # df4pca.to_csv('pca-table.csv')
    df4pca_prescaling = df4pca.drop(['river'], axis=1)

    # Scaling with s-score apporach
    df4pca_final = df4pca_prescaling.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

    # Build PCA
    pca = PCA(n_components=5)
    components = pca.fit_transform(df4pca_final)

    # Get labels for explaind variance respective tot he PC
    labels = {
        str(i): f"PC {i + 1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }
    total_var2d = pca.explained_variance_ratio_.sum() * 100

    np.savetxt('loadings.csv', pca.components_, delimiter=',')

    # Plot data 2-dimensionaly in the new coordinate system of PCs
    fig2d = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(5),
        color=df4pca["river"],
        symbol=df4pca['river'],
        title=f'Total Explained Variance: {total_var2d:.2f}%',
        color_discrete_sequence=px.colors.qualitative.Bold,
        width=1000, height=700,
    )
    fig2d.update_traces(diagonal_visible=False)
    pio.write_image(fig2d, 'pca_matrix.png', scale=4)

    # Plot data 3-dimensionaly in the new coordinate system of PCs
    pca3d = PCA(n_components=3)
    components3d = pca3d.fit_transform(df4pca_final)
    total_var = pca3d.explained_variance_ratio_.sum() * 100
    fig3d = px.scatter_3d(
        components3d, x=0, y=1, z=2, color=df4pca['river'],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # Visualizing loadings of each components
    # pca2d = PCA(n_components=2)
    components2d = pca.fit_transform(df4pca_final)
    total_var2d = pca.explained_variance_ratio_.sum() * 100
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    fig_load = px.scatter(components2d, x=0, y=1, color=df4pca['river'], symbol=df4pca['river'],
                          range_color=[-1000, 1000],
                          width=1000, height=600,
                          labels={'0': 'PC 1', '1': 'PC 2'},
                          color_discrete_sequence=px.colors.qualitative.Bold, )
    feat_annotation = ['IDOC', 'Water level', 'kf', 'T',
                       'Porosity (Wooster)', 'd10', 'd50', 'd90', "S0", 'dm', 'dg',
                       'FSF < 1 mm']
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

