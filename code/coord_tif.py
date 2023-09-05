from osgeo import gdal
import numpy as np

# Open the GeoTIFF file
file_path = 'D:/111/crop.tif'
dataset = gdal.Open(file_path)

# Get the geotransform
geotransform = dataset.GetGeoTransform()

# Extract the latitude and longitude from the geotransform
upper_left_lon = geotransform[0]
upper_left_lat = geotransform[3]
pixel_width = geotransform[1]
pixel_height = geotransform[5]

# Calculate the coordinates for each pixel
rows = dataset.RasterYSize
cols = dataset.RasterXSize

# Create matrices to store latitude and longitude values
latitude_matrix = np.zeros((rows, cols))
longitude_matrix = np.zeros((rows, cols))

for row in range(rows):
    for col in range(cols):
        lon = upper_left_lon + col * pixel_width
        lat = upper_left_lat + row * pixel_height
        latitude_matrix[row, col] = lat
        longitude_matrix[row, col] = lon

# Display the latitude and longitude matrices
print(latitude_matrix)
print(longitude_matrix)

# Close the dataset
dataset = None
