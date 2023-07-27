from riveranalyst.utils.fill_funcs import *


execute_fill_function = {'MeasPosition': fill_measpositions_model,
                         'SubsurfSed': fill_subsurf_model,
                         'SurfSed': fill_surf_model,
                         'IDO': fill_do_model,
                         'Kf': fill_kf_model,
                         'Hydraulics': fill_hydraulics_model,
                         }


def append_db(collected_data, df):
    execute_fill_function[collected_data](df)
