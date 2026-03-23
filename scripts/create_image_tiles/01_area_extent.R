

################################################################################
#
# This code was used for finding the area extent to use when downloading
# images from norgeibilder.no
#
################################################################################

library(terra)
library(sf)

setwd("./data")

area <- vect("Dissolved_polygons_stand_segments.gpkg")

# Check if CRS is WGS84, UTM 32N
crs(area)


# Read polygon layer from GeoPackage file
polygon_layer <- st_read("Dissolved_polygons_stand_segments.gpkg")


polygon_layer <- st_buffer(polygon_layer, 1000)
# Find the bounding box around the entire set of polygons
bbox <- st_bbox(polygon_layer)

bbox



