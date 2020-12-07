# 3D Point Cloud Model of COVID-19

This project will create a 3D point cloud visualization model of the COVID-19 pandemic. The model will focus on modeling the global spatial patterns along with the statistics of different types of live cases for each country by thousands or even millions of georeferenced points.

### Preparation
Check python module/package installation. Uncomment the `pip` statement to install first if any error occurs through import step.


### STEP1: LAND MASK DATA

> You do not need to run `step 1` again because the local `landmask.geojson` has already created. But you are welcomed to uncomment these code cells to run again if needed.

1. Use numpy to populate 2 1-D arrays for Longitude and Latitude respectively. Then use Cartesian Product to create a 2D array representing the Longitude and Latitude pairs of grid points.

2. Convert the 2D array to a temporary dictionary and then load it to Pandas Dataframe.

3. Convert the Pandas Dataframe to GeoPandas Dataframe by creating geometry from the `lon` and `lat` values.

4. Load the shapefile of World Boundaries and create a GeoPandas Dataframe.

5. Perform a `spatial join` between the grid points and the world polygons, and make each point have the values for `Country Name`, `ISO` and location information.

6. Write the spatial join result to a GeoJSON file and save locally.

### STEP2: COVID-19 DATA

> You do not need to run `step 2` again because the local `iso_coords.json` has already created. But you are welcomed to uncomment these code cells to run again if needed.

1. Read the local `landmask.geojson` file, and extract the `ISO` and corresponding `geometry`. 
(There are 172 countries covered in the file.)

2. Request the available countries that have been kept tracking from the COVID-19 API. 
(There are 248 countries kept tracking on the API.)

3. COVID-19 data are stored individually by country with different `slug` mentioned in the request url. Thus, extract the `slug` for the 172 countries and store in `iso_slugs` variable.

4. Loop `iso_slugs` dict and request each country url. Modify the response data by removing usless keys and adding other keys. Store the modified data in local folder `data_by_country` individually. Also provide the request date on the filename.


### STEP3: MODEL DEVELOPMENT
1. Read local COVID-19 data and store in `covid_coords` list. The list involves the coordinates(lon/lat) and case(e.g. latest active cases) for each georeforenced point.

2. Convert the coordinates from Geodetic WGS84(lon/lat) to 3-dimensional Geocentric Cartesian Coordinates(x/y/z). Points are set on the surface of the globe.

3. Use colormap to visualize the `latest active cases` data. In order to have more obvious color distributions, find the minimum and maximum observation values after leaving out the dirty data.

4. Construct the formatted 3D Polygon File Format(PLY) with coordinates and colors for each georeferenced point.
