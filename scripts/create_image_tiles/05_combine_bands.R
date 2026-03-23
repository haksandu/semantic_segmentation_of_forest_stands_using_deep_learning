
################################################################################
#
# This code is used for combining layers of the raster tiles to create a final
# raster composite with five bands (R,G,B,NIR,CHM)
#
################################################################################



# Settings ----------------------------------------------------------------

## Set correct path and working directory

# MEV
folder_path <- "./data/img_tiles/"
wd <- "./data"


# -------------------------------------------------------------------------


library(terra)
library(raster)



# Extract path to images
RGBfiles <- list.files(paste0(folder_path, "rgb/"), pattern = "\\.tif$", full.names = TRUE)
CIRfiles <- list.files(paste0(folder_path, "cir/"), pattern = "\\.tif$", full.names = TRUE)


# Extract the numeric part (assuming it's always before ".tif")
a <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", RGBfiles))
b <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", CIRfiles))

# Sort the vector based on numeric values
RGBfiles <- RGBfiles[order(a)]
CIRfiles <- CIRfiles[order(b)]

rm(a, b)


# Color -------------------------------------------------------------------

# Set wd
setwd(paste0(wd, "/img_tiles/RGBNIR"))

# Combine RGB with NIR from CIR
for(i in 1:length(RGBfiles)){
  
  print(i)
  
  # Define paths
  rgb <- RGBfiles[i]
  cir <- CIRfiles[i]
  
  # Create RGB composite
  rgb_composite <- stack(rgb)
  cir_composite <- stack(cir)
  nir <- cir_composite[[1]]
  
  # Add NIR band as the fourth layer
  rgb_composite <- addLayer(rgb_composite, nir)
  
  # Resample to 1m resolution
  rgb_composite <- raster::aggregate(rgb_composite, fact = 4, fun = mean)
  
  # Write result
  writeRaster(rgb_composite, paste0(getwd(), "/", "tile_", i, ".tif"), format = "GTiff", overwrite = TRUE)
  
}

# Plot one image to see if it looks ok
plotRGB(rgb_composite, r=4, g=1, b=2)
plotRGB(cir_composite, r=1, g=2, b=3)

# Remove unnecessary variables
rm(cir_composite, rgb_composite, nir, RGBfiles, CIRfiles, i, rgb, cir)



# Check if images where created correctly ---------------------------------

# Get path to images
rgbnir <- list.files(paste0(folder_path, "RGBNIR/"), pattern = "\\.tif$", full.names = TRUE)
a <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", rgbnir))
rgbnir <- rgbnir[order(a)]


j <- 0
for(i in rgbnir){
  # Iteration count
  j <- j+1
  cat("Iteration: ", (j + 1), "\n")
  
  # Load image
  img <- rast(i)
  
  # Check number of pixels in image
  if (ncol(img) != 512 || nrow(img) != 512) {
    cat("Image", j, "does not have dimensions 512x512.\n")
  } else {
    print("    Pixels: ok")
  }
  
  # Check image resolution
  if (res(img)[1] != 1 || res(img)[2] != 1) {
    cat("Image", j, "does not have a resolution of 1x1.\n")
  } else {
    print("    Resolution: ok")
  }
}


rm(img, a, j, i, rgbnir)




# Add CHM -----------------------------------------------------------------

# Get CHM tiles
chm <- list.files(paste0(folder_path, "chm/"), pattern = "\\.tif$", full.names = TRUE)
a <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", chm))
chm <- chm[order(a)]

# Get RGBI tiles
rgbnir <- list.files(paste0(folder_path, "RGBNIR/"), pattern = "\\.tif$", full.names = TRUE)
a <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", rgbnir))
rgbnir <- rgbnir[order(a)]

# Set working directory
setwd(paste0(wd, "/img_tiles/images"))

j <- 0
for(i in chm){
  
  j <- j+1
  cat("Iteration: ", j, "\n")
  
  height <- raster(i) 
  spectral <- stack(rgbnir[j])
  
  # check for inf values in chm (some issues occured due to water bodies)
  if(any(is.na(values(height)))){
    height <- reclassify(height, cbind(NA, 0))
  }
  
  # Set same CRS
  if (!same.crs(height, spectral)){
    crs(height) <- crs(spectral)
  }
  
  # Make extent identical
  spectral <- resample(spectral, height, method = "bilinear")
  
  # Make composite
  composite <- addLayer(spectral, height)
  
  # Write result
  writeRaster(composite, paste0(getwd(), "/", "tile_", j, ".tif"), format = "GTiff", overwrite = TRUE)
  
}

rm(height, spectral, composite, chm, j, i)


# Check if the images where created correctly -----------------------------

# Get path to images
stack <- list.files(paste0(folder_path, "images"), pattern = "tile", full.names = TRUE)
a <- as.numeric(gsub(".*tile_(\\d+)\\.tif$", "\\1", stack))
stack <- stack[order(a)]


j <- 0
for(i in stack){
  # Iteration count
  j <- j+1
  cat("Iteration: ", j, "\n")
  
  # Load image
  img <- rast(i)
  
  # Check number of pixels in image
  if (ncol(img) != 512 || nrow(img) != 512) {
    cat("Image", i, "does not have dimensions 512x512.\n")
  } else {
    print("    Pixels:     ok")
  }
  
  
  # Check image resolution
  if (res(img)[1] != 1 || res(img)[2] != 1) {
    cat("Image", i, "does not have a resolution of 1x1.\n")
  } else {
    print("    Resolution: ok")
  }
  
  # Check if number of bands is correct
  if(nlyr(img) != 5){
    cat("Image", i, "does not have 5 layers")
  } else {
    print("    No.bands:   ok")
  }
}



