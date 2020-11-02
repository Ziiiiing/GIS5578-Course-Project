
import numpy as np
import pandas as pd
import geopandas as gpd

# create 1-D arrays for lon and lat
grid_lons = np.arange(-180, 180, 0.5)
grid_lats = np.arange(-90, 90, 0.5)
# cartesian product to pair each lon and lat
grid_coords = [[a, b] for a in grid_lons for b in grid_lats]

# create a temporary dictionary for pandas dataframe
coords_lon = []
coords_lat = []
dict_temp = {'lon': coords_lon, 'lat': coords_lat}

for coord in grid_coords:
    coords_lon.append(coord[0])
    coords_lat.append(coord[1])


points = pd.DataFrame.from_dict(dict_temp)
# generate the geometry from lon/lat columns
points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.lon, points.lat))
polygons = gpd.read_file('World_Boundaries/World_Countries_(Generalized).shp')

# keep the same coordinate reference system
points = points.set_crs('EPSG:4326')
polygons = polygons.to_crs('EPSG:4326')

# spatial join
land = gpd.sjoin(points, polygons, how='inner', op='intersects')
land = land.drop(columns=['lon', 'lat', 'index_right'])

# write geojson
land.to_file('land.geojson', driver='GeoJSON')