import rasterio
from rasterio.plot import show

# Path to the GeoTIFF file
file_path = "D:/111/result/Himawari_LST_vietnam_0612.tif"

# Open the GeoTIFF file
with rasterio.open(file_path) as src:
    # Read band 1 data
    band1_data = src.read(1)

    # Show the band 1 data
    # show(band1_data)
print(file_path)
print(band1_data[17][43])
