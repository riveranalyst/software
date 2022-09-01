from . import fill_subsurf_tab, \
    fill_stations_tab, \
    fill_do_tab, \
    fill_surf_tab, \
    fill_kf_tab, \
    fill_hydraulics_tab

execute_fill_function = {'SubsurfSed': fill_subsurf_tab.fill_subsurf_model,
                         'SurfSed': fill_surf_tab.fill_surf_model,
                         'IDO': fill_do_tab.fill_do_model,
                         'kf': fill_kf_tab.fill_kf_model,
                         'Hydraulics': fill_hydraulics_tab.fill_hydraulics_model,
                         }


def append_db(collected_data, df):
    execute_fill_function[collected_data](df)
