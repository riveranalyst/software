from . import fill_subsurf_tab, fill_stations_tab, fill_do_tab

execute_fill_function = {'SubsurfSed': fill_subsurf_tab.fill_fc_model,

                             #TODO
                             # 'SurfSed': fill_surfsed_model,

                             'DO': fill_do_tab.fill_do_model
                             }


def append_db(collected_data, df):
    execute_fill_function[collected_data](df)