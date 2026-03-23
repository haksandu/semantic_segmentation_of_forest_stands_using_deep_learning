

################################################################################
#
# This code is used for creating a list over RGB and CIR tiles downloaded from
# norgeibilder.no
#
################################################################################



library(terra)

# RGB ---------------------------------------------------------------------



# Define path to RGB images
folder_path <- "./data/"

# Create list over all images
FileList <- list.files(paste0(folder_path, "Oslo-Ostlandet_2022_MEV_RGB/"), pattern = "\\.tif$", full.names = TRUE)

# Load aoi outline, and crop by vector
aoi <- vect(paste0(folder_path, "Dissolved_polygons_stand_segments.gpkg"))

# Check for intersection with aoi
files <- c()
j <- 0

for(i in FileList){
  j <- j+1
  print(j)
  img <- rast(i)
  if(is.related(img, aoi, 'intersects')){
    files <- c(files, i)
  }
}

# Extract the numeric part (assuming it's always before ".tif")
f <- as.numeric(gsub(".*-(\\d+)\\.tif", "\\1", files))

# Sort the vector based on numeric values
files <- FileList[order(f)]

# Save list as .txt file
writeLines(files, paste0(folder_path, "img_list_rgb.txt"))




# CIR ---------------------------------------------------------------------


# Define path to CIR images
folder_path <- "./data/"


# Create list over all images
FileList <- list.files(paste0(folder_path, "Oslo-Ostlandet_2022_MEV_CIR/"), pattern = "\\.tif$", full.names = TRUE)


# Load aoi outline, and crop by vector
aoi <- vect(paste0(folder_path, "Dissolved_polygons_stand_segments.gpkg"))


# Check for intersection with aoi
files <- c()
j <- 0

for(i in FileList){
  j <- j+1
  print(j)
  img <- rast(i)
  if(is.related(img, aoi, 'intersects')){
    files <- c(files, i)
  }
}

# Extract the numeric part (assuming it's always before ".tif")
f <- as.numeric(gsub(".*?(\\d+)\\.tif", "\\1", files))

# Sort the vector based on numeric values
files <- files[order(f)]

# Save list as .txt file
writeLines(files, paste0(folder_path, "img_list_cir.txt"))










