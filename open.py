import rasterio
import matplotlib.pyplot as plt

# Open the GeoTIFF file
file_path = 'vietnam.tif'
dataset = rasterio.open(file_path)

# Access the raster data
raster_data = dataset.read(1)  # Assuming you want to read the first band

print(raster_data)

# Get information about the raster
width = dataset.width
height = dataset.height
count = dataset.count
crs = dataset.crs
transform = dataset.transform

# Close the dataset
dataset.close()

# Print information about the raster
print("Raster Width:", width)
print("Raster Height:", height)
print("Number of Bands:", count)
print("Coordinate Reference System:", crs)
print("Geo-Transform:", transform)

# Perform any required data processing or analysis on the raster data
# ...

# Plot the raster data
plt.imshow(raster_data, cmap='rainbow')
plt.colorbar(label='Pixel Value')

# Show the plot
plt.show()
