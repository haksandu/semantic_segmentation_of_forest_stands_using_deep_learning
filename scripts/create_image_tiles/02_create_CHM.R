

################################################################################
#
# This code was used for calculating a 1x1m CHM
# The final output is a CHM vrt
#
################################################################################



# Load packages
library(lidR)
library(terra)
library(mapview)
library(sf)


# Laser point cloud -------------------------------------------------------
ctg <- readLAScatalog(".data//LAS-data/LAS/")

# # Set crs using EPSG code 
st_crs(ctg) <- st_crs(32632)


# summary of catalog
ctg

# View map
mapview(st_as_sf(ctg))


# Check acquisition date --------------------------------------------------

# Year
year <- 2021

# Get day of year
doy <- as.numeric(summary(ctg@data$File.Creation.Day.of.Year)["Min."])

# Convert to Date
acquisition_date <- as.Date(doy - 1, origin = paste0(year, "-01-01")) # -1 becuase 01.01 is indexed 1

# Print the date
print(acquisition_date)

# -------------------------------------------------------------------------


# summary of catalog
ctg

# View map
mapview(st_as_sf(ctg))

# Add buffer 
opt_chunk_buffer(ctg) <- 5 

# Set output path
opt_output_files(ctg) <- "./data/ALS_CHM/intermediate/raw_tiles/{ORIGINALFILENAME}_{ID}"



# Create CHM --------------------------------------------------------------

# canopy height model (1m resolution)
chm <- rasterize_canopy(ctg, res=1, algorithm = p2r(0.2, na.fill = tin()))
plot(chm)

#crs(chm) <- crs("+proj=utm +zone=32 +datum=WGS84 +units=m +no_defs")


# Check if any NA values
has_na_values <- any(is.na(values(chm)))
print(paste("Contains NA values:", has_na_values))


# Create VRT
files <- dir("./data/chm/tmp/", pattern = "\\.tif$", full.name=TRUE)
vrt_chm <- terra::vrt(files, filename="./data/chm/chm_mev.vrt")





# Check if any NA values
has_na_values <- any(is.na(values(chm)))
print(paste("Contains NA values:", has_na_values))


