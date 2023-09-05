import rasterio
import glob
import kernel_functions as kf
import pandas
import numpy as np
from numpy import zeros, newaxis


path_emis31 = glob.glob("D:/111/emis31.tif")
path_emis32 = glob.glob("D:/111/emis32.tif")
path_h09 = glob.glob("D:/111/data/H09_crop/NC_H09_20230618_0000_R21_FLDK.06001_06001.tif")
path_csv = 'D:/111/data/MOD08/MOD08_E3_vapor.csv'
pathRef = 'D:/111/vietnam.tif'

pathLST = 'D:/111/result/'

factor = {'c':45.257935, 'a1':0.985361, 'a2':1.332220, 'a3':-41.750015, 'd':0.035390}
factor2 = {'c':52.651920, 'a1':0.930713, 'a2':2.402630, 'a3':-35.962742, 'd':-0.219514}

with rasterio.open(pathRef) as src:
    kwargs = src.meta.copy()
    kwargs['count'] = 1
    kwargs['compress'] ='lzw'
    kwargs['nodata'] = 0

sf = kf.kernel()

vapor = pandas.read_csv(path_csv)
vap = vapor.loc[vapor['Date'] == '2023-06-18']
if vap.shape[0] > 0:
    vapRef = np.float32(vap.iloc[[0]]['Vapor_mean_mean'])[0]/1000

if len(path_emis31) > 0:            
    data = rasterio.open(path_emis31[0])
    emis31 = data.read(1)
    
if len(path_emis31) > 0:            
    data = rasterio.open(path_emis31[0])
    emis32 = data.read(1)
    
emis = (emis31 + emis32)/2*0.002 + 0.49


if len(path_h09) > 0:            
    data = rasterio.open(path_h09[0])
    b14 = data.read(1)
    b15 = data.read(2)
    soz = data.read(3)
    
if vapRef <= 2.0:
    lst = sf.calculateLST(b14, b15, soz , emis, emis31, factor)
else:
    lst = sf.calculateLST(b14, b15, soz , emis, emis31, factor2)
    
lst[lst < 0] = 0

print(lst)

fileNameBand = pathLST + "Himawari_LST_vietnam_0618.tif"

lst2 = lst[newaxis, :, :]
with rasterio.open(fileNameBand, "w", **kwargs) as dest:
    dest.write(lst2)
