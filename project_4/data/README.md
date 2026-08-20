# About this data

Wildfire data set is taken from National Interagency Fire Center. 
https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-wildland-fire-locations-full-history/explore?filters=eyJEYWlseUFjcmVzIjpbMCwxMDMyNjQ4XSwiQ2FsY3VsYXRlZEFjcmVzIjpbMCw5NjM0MDUuMzUwNF19&location=43.428881%2C-120.156002%2C7.00

I filtered it approximately to the boundaries of Oregon,
then added "easting" and "northing" columns so that
we can get accurate distances between points.
(See add_utm.py for adding easting, northing to a CSV dataset with
latitude and longitude.)

Map of Oregon is from Wikimedia Commons: 
https://commons.wikimedia.org/wiki/File:USA_Oregon_location_map.svg

This is an equirectangular projection.
There will be distortion in georeferencing
the map based on UTM coordinates (easting and northing), 
but it shouldn't be _too_ bad for the extent
of Oregon. 

Boundaries as given on Wikimedia data page: 
Equirectangular projection, 
N/S stretching 140.0 %. 
Geographic limits of the map:
N: 46.5° N
S: 41.8° N
W: 124.9° W
E: 116.3° W

UTM equivalents in Zone 10T
Origin    (-124.9, 41.8) =  342151, 4629315 10T
NE corner (-116.3, 46.5) = 1014041, 5171453 10T

Plausibility check per Google Maps:
Astoria (NW) is 46.1916701,-123.955342
Brookings (SW) is 42.0741729,-124.3407476
Boise ID (E) is 43.6000263,-116.7752622

In pixels (Oregon.png):  1024x783
