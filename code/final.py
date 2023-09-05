import rasterio

# File path
output_tiff_file = "D:/111/data/H09_crop/NC_H09_20230610_0000_R21_FLDK.06001_06001.tif"

# Read the GeoTIFF file
with rasterio.open(output_tiff_file) as src:
    # Get the bounding box (spatial extent)
    bounds = src.bounds
    # Get the file size (number of rows and columns)
    rows, cols = src.shape

# Create arrays for latitude and longitude bounds
latitude_bounds = [bounds.bottom, bounds.top]
longitude_bounds = [bounds.left, bounds.right]

# Display latitude and longitude bounds and file size as arrays
print("Latitude bounds: ", latitude_bounds)
print("Longitude bounds: ", longitude_bounds)
print("File size (rows, cols): ", (rows, cols))
