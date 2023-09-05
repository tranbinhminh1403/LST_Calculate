# -*- coding: utf-8 -*-

import osgeo.gdal as gdal
import glob, itertools, os, datetime
import rasterio.mask as mp
import numpy.ma as ma
from rasterio import crs
from affine import Affine
import os, sys
import csv, glob, itertools, getopt
import kernel_functions as kf
import numpy as np
from collections import OrderedDict


pathOrigin = '/shared/rsg/projects/himawari/Test_MOD08_E3/'
pathCSV = '/shared/rsg/projects/himawari/Test_MOD08_E3/CSV/'


dy = [str(item).zfill(2) for item in map(str, range(1,32))]
hr = [str(item).zfill(2) for item in map(str, range(0,24))]
mn = [str(item).zfill(2) for item in map(str, range(0,60,10))]

#yr = ['2016', '2017']
yr = [str(item).zfill(4) for item in map(str, range(2023, 2023))]
#mt = ['02']
mt = [str(item).zfill(2) for item in map(str, range(1,13))]
#mt

p1 = [-33.5, 150.5]
geoTrans_org = (-180.0, 1.0, 0.0, 90.0, 0.0, -1.0)
sf = kf.kernel()
rowcol = sf.world2Pixel(geoTrans_org, p1[1], p1[0])
#a2 = gdset.ReadAsArray(rowcol[0],rowcol[1],2,2)

os.chdir(pathCSV)
with open('MOD08_E3_vapor_Sydney.csv', 'w') as csvfile:
    #print('Writing out to: {}/report_withCloud.csv'.format(os.getcwd()))
    #fieldnames = ["col","row","band","date","time","BRF","sa","sz","invalidmask"]
    fieldnames = OrderedDict([('Date', None),('Vapor_mean_mean', None)])
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for yr1, mt1, dy1 in itertools.product(yr, mt, dy):
        try:
            doy = datetime.datetime.strptime(yr1 + mt1 + dy1, "%Y%m%d").date().strftime('%j')
            l1 = glob.glob(pathOrigin + 'MYD08_E3*' + yr1 + doy + '*hdf')
            #l2 = glob.glob(pathMYD11A2_WGS + 'MYD11A2*' + yr1 + doy + '*h30v12*Emis_32*tif')
            #print(pathMYD11A2_WGS + 'MYD11A2*' + yr1 + doy + '*h30v12*Emis_31*tif')
            if len(l1)>0:
                print(l1[0])
                #print(l2[0])
                subdataset = gdal.Open(l1[0]).GetSubDatasets()
                gdset = gdal.Open(subdataset[1022][0])
                a2 = np.mean(gdset.ReadAsArray(rowcol[0],rowcol[1],2,2))
                print(a2)
                writer.writerow({'Date': '{}-{}-{}'.format(yr1,mt1,dy1),
                                 'Vapor_mean_mean': float(a2)})
        except:
            print("Error at "+ yr1 + mt1 + dy1)
        