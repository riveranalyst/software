import os
import django
from pathlib import Path
import numpy as np
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from pyproj import transform, CRS


BASE_DIR = Path(__file__).resolve().parent.parent


def convert_coord_for_mapbox(df):
    outproj = 'epsg:4326'
    df['lat_mapbox'] = np.nan
    df['lon_mapbox'] = np.nan
    for index, row in df.iterrows():
        if row.coord_system == outproj:
            row.lat_mapbox = row.lat
            row.lon_mapbox = row.lon

        # for epsg:31468, the easting and northing are inversed, see https://epsg.io/31468
        if row.coord_system == 'epsg:31468':
            row.lon_mapbox, row.lat_mapbox = transform(
                row.coord_system, outproj, row.lat, row.lon)
        else:
            row.lon_mapbox, row.lat_mapbox = transform(
                row.coord_system, outproj, row.lon, row.lat)
    return df
