import osgeo.gdal as gdal
import rasterio, fiona
import rasterio.mask as mp
import numpy.ma as ma
from rasterio import crs
from affine import Affine
import os, sys
import csv, glob, itertools, getopt
import kernel_functions as kf
import numpy as np
from collections import OrderedDict
import netCDF4 as nc
import pandas
from numpy import zeros, newaxis


factor = {'c':45.257935, 'a1':0.985361, 'a2':1.332220, 'a3':-41.750015, 'd':0.035390}
factor2 = {'c':52.651920, 'a1':0.930713, 'a2':2.402630, 'a3':-35.962742, 'd':-0.219514}
vapor_fin = 1.0

#hanoi coordinate
p1 = [0,0]

path_tif = 'D:/111/crop_ver4.tif'
path_vapor = 'D:/111/data/MOD08/MOD08_E3.A2023169.061.2023177223923.hdf'
path_hm = 'D:/111/data/H09/NC_H09_20230610_0000_R21_FLDK.06001_06001.nc'
path_modis = 'D:/111/data/MOD11A2/MOD11A2.A2023169.h27v06.061.2023178033326.hdf'
path_csv = 'D:/111/data/MOD08/MOD08_E3_vapor.csv'

pathLST = 'D:/111/result/'

output_path = 'D:/111/result.txt'


with rasterio.open(path_tif) as src:
    kwargs = src.meta.copy()
    kwargs['count'] = 1
    kwargs['compress'] ='lzw'
    kwargs['nodata'] = 0

#read crop.tif coord
dataset = gdal.Open(path_tif)


geotransform = dataset.GetGeoTransform()


upper_left_lon = geotransform[0]
upper_left_lat = geotransform[3]
pixel_width = geotransform[1]
pixel_height = geotransform[5]

rows = dataset.RasterYSize
cols = dataset.RasterXSize

LST = np.zeros((rows, cols), dtype=np.float64)

# Create matrices to store latitude and longitude values
# latitude_matrix = np.zeros((rows, cols), dtype=np.float64)
# longitude_matrix = np.zeros((rows, cols), dtype=np.float64)

for row in range(rows):
    for col in range(cols):
        lon = upper_left_lon + col * pixel_width
        lat = upper_left_lat + row * pixel_height
        # latitude_matrix[row, col] = lat
        # longitude_matrix[row, col] = lon
        
        p1[0] = lat
        p1[1] = lon
        

        subdataset = gdal.Open(path_vapor).GetSubDatasets()
        gdset = gdal.Open(subdataset[1022][0])

        geoTrans_org = (-180.0, 1.0, 0.0, 90.0, 0.0, -1.0)
        sf = kf.kernel()
        rowcol = sf.world2Pixel(geoTrans_org, p1[1], p1[0])
        vapor = np.mean(gdset.ReadAsArray(rowcol[0], rowcol[1], 2, 2))
        a2 = gdset.ReadAsArray(rowcol[0], rowcol[1], 2, 2)




        subdataset_emis = gdal.Open(path_modis).GetSubDatasets()

        gdset = gdal.Open(subdataset[8][0])

        rowcol_emis31 = sf.world2Pixel(geoTrans_org, p1[1], p1[0])
        emis31 = np.mean(gdset.ReadAsArray(rowcol[0], rowcol[1], 2, 2))



        gdset = gdal.Open(subdataset[9][0])

        rowcol_emis32 = sf.world2Pixel(geoTrans_org, p1[1], p1[0])
        emis32 = np.mean(gdset.ReadAsArray(rowcol[0], rowcol[1], 2, 2))

        dataset = nc.Dataset(path_hm)

        latitude = dataset.variables['latitude'][:]
        longitude = dataset.variables['longitude'][:]


        lat_index = int((p1[0] - latitude[0]) / (latitude[1] - latitude[0]))

        lon_index = int((p1[1] - longitude[0]) / (longitude[1] - longitude[0]))

        tbb_14 = dataset.variables['tbb_14'][:]


        tbb_14_value = tbb_14[lat_index, lon_index]





        tbb_15 = dataset.variables['tbb_15'][:]
        tbb_15_value = tbb_15[lat_index, lon_index]



        soz = dataset.variables['SOZ'][:]
        soz_value = soz[lat_index, lon_index]



        vapor_fin = vapor / 1000
        emis = (emis31 + emis32)/2*0.002 + 0.49

        if vapor_fin <= 1.0:
            lst = sf.calculateLST(tbb_14_value, tbb_15_value, soz_value , emis, emis31, factor)
        else:
            lst = sf.calculateLST(tbb_14_value, tbb_15_value, soz_value , emis, emis31, factor2)

        lst = "{:.2f}".format(lst)
        LST[row, col] = float(lst)

        print(row, col)
        print(lst)

        # with open(output_path, 'w') as file:
        #     file.write(lst + ',')
        fileNameBand = pathLST + "Himawari_LST_vietname_0610.tif"
        
        # lst2 = lst[newaxis, :, :]
        with rasterio.open(fileNameBand, "w", **kwargs) as dest:
            dest.write(LST, 1)








