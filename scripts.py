'''
	Code submission #1
	@author: Gene/Ziying Cheng

'''

import numpy as np
import pandas as pd
import geopandas as gpd
import json
from math import cos, sin, pi
import open3d as o3d

# Step 1: Land Mask Data ------------------------------
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


####
# Step 2: COVID-19 Data ---------------------------------
# Request live data by countries with all cases from API
# Spatial Join with land points to correct lon/lat
# Store in local JSON file
####


# Step 3: Model Development -----------------------------
# convert the coordinates from lon/lat to x/y/z
def coords_conversion(lon, lat, num):
    O = [0, 0, 0]  # center
    R = 6400       # radius
    S = 0.01       # scale
    # D = 3        # height exaggeration
    
    # calculate the radian of the sphere
    rad_lat, rad_lon = lat * pi / 180, lon * pi / 180

    # calculate the cartesian coordiantes of each point
    x = O[0] + S * R * cos(rad_lat) * cos(rad_lon)
    y = O[1] + S * R * cos(rad_lat) * sin(rad_lon)
    z = O[2] + S * R * sin(rad_lat)

    return (x, y, z)

# write ply file for 3D model
def model(path):
    with open(path, 'w') as fw:
    # write headers with required format 
        fw.write('ply\nformat ascii 1.0\n')
        fw.write('element vertex %d\n' % len(coords))
        fw.write('property float x\n')
        fw.write('property float y\n')
        fw.write('property float z\n')

        if len(colors) == len(coords):
            fw.write('property uchar red\n')
            fw.write('property uchar green\n')
            fw.write('property uchar blue\n')

        fw.write('end_header\n')
        
        # write data
        if len(colors) == len(coords):
            for coord, color in zip(coords, colors):
                fw.write("%f %f %f %d %d %d\n" % (
                    coord[0],
                    coord[1],
                    coord[2],
                    color[0],
                    color[1],
                    color[2]
                    ))
        else:
            for coord in coords:
                fw.write("%f %f %f\n" % (
                    coord[0],
                    coord[1],
                    coord[2]
                    ))
        print('##### PLY model created #####')


# read geojson and store in the variable 'data'
with open('land.geojson') as f:
    data = json.load(f)

# extract values of the 'features' key
features = data['features']

# retrieve lons/lats from each feature
lons = []
lats = []
for feature in features:
    geometry = feature['geometry']
    coord = geometry['coordinates']
    lats.append(coord[0])
    lons.append(coord[1])


coords = []
colors = []

# store coord and color for each point 
coords.extend([ coords_conversion(lat, lon, 0) for lon, lat in zip(lons, lats) ]) 
colors.extend([ (192,192,192) for x in lats ])

# create land(base) model
model('model_py.ply')

# read and display model
PC = o3d.io.read_point_cloud('model_py.ply')
o3d.visualization.draw_geometries([PC])

####
# Step 4: Model Advanced Properties
#
#
####