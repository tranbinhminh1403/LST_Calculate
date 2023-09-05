require(raster)

# Vietnam extent
ext_Vietnam <- extent(101.538891425, 107.711666693, 20.696211560, 23.392692567)

# File paths
input_nc_file <- "D:/111/data/H09/NC_H09_20230613_2350_R21_FLDK.06001_06001.nc"
output_tiff_file <- "D:/111/data/H09_crop/NC_H09_20230613_0000_R21_FLDK.06001_06001.tif"
# Read NetCDF file for tbb_14
lst_tbb_14 <- raster(input_nc_file, varname = 'tbb_14')

# Read NetCDF file for tbb_15
lst_tbb_15 <- raster(input_nc_file, varname = 'tbb_15')

lst_soz <- raster(input_nc_file, varname = 'SOZ')

# Crop both variables to Vietnam extent and convert temperature data from Kelvin to Celsius
lst_tbb_14_crop <- crop(lst_tbb_14, ext_Vietnam) 
lst_tbb_15_crop <- crop(lst_tbb_15, ext_Vietnam) 
lst_soz <- crop(lst_soz, ext_Vietnam) 

# Create a RasterBrick to hold both tbb_14 and tbb_15
lst_brick <- brick(lst_tbb_14_crop, lst_tbb_15_crop, lst_soz)

# Write output raster as GeoTIFF with both tbb_14 and tbb_15
writeRaster(lst_brick, output_tiff_file, format = 'GTiff', overwrite = TRUE)

# Print information
print(lst_brick)
