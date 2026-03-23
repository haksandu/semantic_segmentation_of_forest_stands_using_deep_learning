

################################################################################
#
# This code is used for dividing the rasterized stand polygons into final tiles.
#
################################################################################


# This code requires that the polygon layer has been rasterized in GIS
# Raster > Conversion > Rasterize
#   - Get Values: "HOGSTKLASSE"
#   - Units of Outdata: Georeferenced units
#   - W/H: 1m
#   - Extent > From Layer > select indata layer
#   - Non-data value: 0


# Settings ----------------------------------------------------------------

## Set correct path

# MEV
folder_path <- "./data/"
wd <- "./data/img_tiles"

# Select grid size
gr <- "512_grid.gpkg"






# -------------------------------------------------------------------------

# Load packages
library(terra)



# Masks from raster -------------------------------------------------------


# Load data
VRT <- vrt(paste0(folder_path, "stands_2022/stand_2022_raster.tif"))
res(VRT)
grid <- vect(paste0(folder_path, gr))

# Plot data
plot(VRT)
lines(grid, col='red', lwd=2)


# Check crs
crs1 <- crs(VRT)
crs2 <- crs(grid)

same_crs <- same.crs(crs1, crs2)
if (same_crs) {
  print("Both layers have the same CRS.")
} else {
  print("The CRS of the layers differs.")
}


# Make tiles
setwd(paste0(wd, "/mask_temp"))
c <- makeTiles(VRT, grid, overwrite=TRUE)


rm(c, VRT)



# Processing tiles --------------------------------------------------------

# Find paths to images and sort by number
mask <- list.files(paste0(folder_path, "img_tiles/mask_temp/"), pattern = "\\.tif$", full.names = TRUE)
a <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", mask))
mask <- mask[order(a)]


### Replace NA's with zero

# set working directory
setwd(paste0(wd, "/mask"))

j <- 0
for(i in mask){
  
  # Update counter
  j <- j+1
  cat("Iteration: ", j, "\n")
  
  # Load image
  img <- rast(i)
  
  # Check if image contains NA's
  # Set NA's to zero
  if(any(is.na(values(img)))){
    img[is.na(img[])] <- 0
    cat("NA's swapped with zero \n")
  }
  writeRaster(img, paste0("tile_", j, ".tif"), overwrite=TRUE)
}


