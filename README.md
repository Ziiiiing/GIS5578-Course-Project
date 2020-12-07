# 3D Point Cloud Model of COVID-19

This project will create a 3D point cloud visualization model of the COVID-19 pandemic. The model will focus on modeling the global spatial patterns along with the statistics of different types of live cases for each country by thousands or even millions of georeferenced points.


### Step 1: Generate Land Mask Points
1. Use numpy to populate 2 1-D arrays for Longitude and Latitude respectively. Then use Cartesian Product to create a 2D array representing the Longitude and Latitude pairs of grid points.

2. Convert the 2D array to a temporary dictionary and then load it to Pandas Dataframe.

3. Convert the Pandas Dataframe to GeoPandas Dataframe by creating geometry from the `lon` and `lat` values.

4. Load the shapefile of World Boundaries and create a GeoPandas Dataframe.

5. Perform a `spatial join` between the grid points and the polygon, and make each point have the values for `Country Name`, `ISO` and location information.

6. Write the spatial join result to a GeoJSON file and save locally.

### Step 2: Coordinate Conversion
1. Read the `land.geojson` and extract the geometry information for land mask points.

2. Convert the longitude/latitude to Cartesian Coordinates X/Y/Z. Since the land mask points do not have to represent any covid-19 data, thus the `num` should be `0` and the `z` value is set to the distance from the land to the earth origin.

3. Extend the Cartesian Coordinates into `coords` list and also extended a default color into `colors` list according to the PLY model format.

### Step 3: Model Development (Land Mask Points)
1. Write the PLY file to create the 3D model for land mask points.

2. Use open3d library to read the ply file and display 3D model locally.