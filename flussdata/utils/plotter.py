import plotly.graph_objs as go
import plotly.express as px
from django_pandas.io import read_frame


def plot_gsd(subsurf_sample, title):
    # graph embbeded ina  div to return to the template:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis_title='Grain size [mm]',
        yaxis_title='Percent finer [%]',
        # height=420,  # if height and width are given, the figure is not resized within the div when user zooms in/out
        # width=560,
        margin={"r": 30, "t": 30, "l": 30, "b": 30},
        yaxis=dict(showline=True,
                   ticks='outside',
                   range=[0, 100]),

        xaxis=dict(showline=True,
                   ticks='outside',
                   type="log"
                   # range=[0.063, 250]
                   )
    )

    for fc in subsurf_sample:
        ds = ['250', '125', '63', '31_5', '16', '8', '4', '2', '1', '0_5', '0_25', '0_125', '0_063', '0_031']
        ds_float = [250, 125, 63, 31.5, 16, 4, 2, 1, 0.5, 0.25, 0.125, 0.063, 0.031]
        ds_values = []

        # loop through the sediment fractions, which are column names in the db
        for d in ds:
            ds_values.append(eval('fc.percent_finer_{0}mm'.format(d)))

        # create graph
        fig.add_trace(go.Scatter(x=ds_float, y=ds_values,
                                 mode='lines', name='test',
                                 opacity=0.8,
                                 hovertext=fc.sample_id,
                                 ))
    return fig


def plot_ido(idocs):
    fig_idoc = go.Figure()
    fig_idoc.update_layout(
        xaxis_title='Dissolved oxygen concentration [mg/L]',
        yaxis_title='Riverbed depth [m]',
        # height=560,
        # width=420,
        margin={"r": 30, "t": 30, "l": 30, "b": 30})
    idoc_df = read_frame(idocs)
    for idoc in idoc_df['sample_id'].unique():
        idoc_sample = idoc_df[idoc_df['sample_id'] == idoc]
        fig_idoc.add_trace(go.Scatter(x=idoc_sample['idoc_mgl'],
                                      y=idoc_sample['sediment_depth_m'],
                                      mode='lines',
                                      hovertext=idoc_sample['sample_id'],
                                      ))
    fig_idoc.update_layout(yaxis=dict(showline=True,
                                      ticks='outside',
                                      range=[0.55, 0],
                                      tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5]
                                      ),
                           xaxis=dict(showline=True,
                                      ticks='outside',
                                      range=[0, 13],
                                      tickvals=[0, 2, 4, 6, 8, 10, 12],
                                      side='top'
                                      ))
    return fig_idoc


def plot_map(df_stations):
    fig = px.scatter_mapbox(df_stations,
                            lat='y_epsg4326',
                            lon='x_epsg4326',
                            # hover_name='sample_id',
                            color='name',
                            zoom=10,
                            # size='d50',
                            )
    fig.update_layout(
        mapbox_style="open-street-map",
        legend_title_text='Stations'
    )
    fig.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10})
    return fig