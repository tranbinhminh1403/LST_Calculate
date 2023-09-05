# -*- coding: utf-8 -*-

#from osgeo import gdal, gdalconst
import rasterio, glob, itertools, os, datetime
import pandas
import numpy as np
from rasterio import Affine as A
import kernel_functions as kf
#from rasterio.warp import calculate_default_transform, reproject, RESAMPLING
from rasterio.warp import calculate_default_transform, reproject, Resampling
from numpy import zeros, newaxis

#Reproject Himawaridata
a1 = {'proj': 'longlat', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}
a2 = {'proj': 'geos', 'lon_0': 140.7, 'h': 35785863, 'x_0':0,
      'y_0': 0, 'a':6378137, 'b':6356752.3, 'no_defs': True}
a3 = {'proj': 'sinu', 'lon_0': 0, 'x_0':0,
      'y_0': 0, 'a':6371007.181, 'b':6371007.181, 'no_defs': True}

proj1 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs '
proj2 = '+proj=geos +lon_0=140.7 +h=35785863 +x_0=0 +y_0=0 +a=6378137 +b=6356752.3 +units=m +no_defs'
proj3 = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"


dy = [str(item).zfill(2) for item in map(str, range(1,32))]
hr = [str(item).zfill(2) for item in map(str, range(0,24))]
mn = [str(item).zfill(2) for item in map(str, range(0,60,10))]

yr = ['2017']
mt = ['02']

pathMYD11A2_WGS = '/shared/c3/projects/himawari/MYD11A2_Sydney_WGS84_001/RemoveNull/'   
pathH8_WGS = '/shared/c3/projects/himawari/Sydney_Himawari_WGS84_001/'
pathRef = '/shared/c3/projects/himawari/Sydney_map_ref/Sydney_raster_WGS84_001.tif'

pathLST = '/shared/c3/projects/himawari/Syndey_LST_calculated/'
#pathRef = 'C:/ownCloud/Map_Vector/Sydney/Sydney_raster_WGS84_0005.tif'
with rasterio.open(pathRef) as src:
    kwargs = src.meta.copy()
    kwargs['count'] = 1
    kwargs['compress'] ='lzw'
    kwargs['nodata'] = -10000

emis31 = rasterio.open('/shared/c3/projects/himawari/MYD11A2_Sydney_WGS84_001/RemoveNull/MYD11A2.A2017025.h30v12.RemoveNull.Emis_31_Sydney.tif').read(1)
emis32 = rasterio.open('/shared/c3/projects/himawari/MYD11A2_Sydney_WGS84_001/RemoveNull/MYD11A2.A2017025.h30v12.RemoveNull.Emis_32_Sydney.tif').read(1)

emis = (emis31 + emis32)/2*0.002 + 0.49
factor = {'c':45.257935, 'a1':0.985361, 'a2':1.332220, 'a3':-41.750015, 'd':0.035390}
factor2 = {'c':52.651920, 'a1':0.930713, 'a2':2.402630, 'a3':-35.962742, 'd':-0.219514}

pathCSV = '/shared/c3/projects/himawari/Test_MOD08_E3/CSV/MOD08_E3_vapor_Sydney.csv'
vapor = pandas.read_csv(pathCSV)
sf1 = kf.kernel()
#sf1 = kernel()
vapRef = 1.0
for yr1, mt1, dy1 in itertools.product(yr, mt, dy):
    vap = vapor.loc[vapor['Date'] == yr1 +'-' + mt1 + '-' + dy1]
    if vap.shape[0] > 0:
        vapRef = np.float32(vap.iloc[[0]]['Vapor_mean_mean'])[0]/1000
    
    doy = datetime.datetime.strptime(yr1 + mt1 + dy1, "%Y%m%d").date().strftime('%j')
    l1 = glob.glob(pathMYD11A2_WGS + 'MOD11A2*' + yr1 + doy + '*h27v06*Emis_31*tif')
    l2 = glob.glob(pathMYD11A2_WGS + 'MOD11A2*' + yr1 + doy + '*h27v06*Emis_32*tif')
    #print(pathMYD11A2_WGS + 'MYD11A2*' + yr1 + doy + '*h30v12*Emis_31*tif')
    if len(l1)>0 and len(l2)>0:
        print(l1[0])
        #print(l2[0])
        emis31 = rasterio.open(l1[0]).read(1)
        emis32 = rasterio.open(l2[0]).read(1)
        emis = (emis31 + emis32)/2*0.002 + 0.49

    for hr1, mn1 in itertools.product(hr, mn):
        l3 = glob.glob(pathH8_WGS + 'Hanoi_Bands_forLST_' + yr1 + mt1 + dy1 + '_' + hr1 + mn1 + '*.tif')
        if len(l3)>0:            
            data = rasterio.open(l3[0])
            b14 = data.read(2)
            b15 = data.read(3)
            sza = data.read(4)
            if vapRef <= 1.0:
                lst = sf1.calculateLST(b14, b15, sza, emis, emis31, factor)
            else:
                lst = sf1.calculateLST(b14, b15, sza, emis, emis31, factor2)
            fileNameBand = pathLST + "Hanoi_Himawari_LST_" + yr1 + mt1 + dy1 + '_' +  hr1+mn1 + '.tif'
            #print(lst.shape)
            #print(fileNameBand)
            #print(kwargs)
            #print(lst)
            lst2 = lst[newaxis, :, :]
            with rasterio.open(fileNameBand, "w", **kwargs) as dest:
                dest.write(lst2)
            
            
