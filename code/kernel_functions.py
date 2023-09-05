# -*- coding: utf-8 -*-
import numpy as np
import statsmodels.api as sm
import math
from pyproj import Proj, transform

class kernel:
    def reg_m(self, y, x):
        """
        This function is to generate OLS model for BRDF kernel calculation
        """
        ones = np.ones(len(x[0]))
        X = sm.add_constant(np.column_stack((x[0], ones)))
        for ele in x[1:]:
            X = sm.add_constant(np.column_stack((ele, X)))
        results = sm.OLS(y, X).fit()
        return results
    
    def world2Pixel(self, geoMatrix, x, y):
        #"""
        #Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
        #the pixel location of a geospatial coordinate
        #"""
        ulX = geoMatrix[0]
        ulY = geoMatrix[3]
        xDist = geoMatrix[1]
        yDist = geoMatrix[5]
        #rtnX = geoMatrix[2]
        #rtnY = geoMatrix[4]
        column = int((x - ulX) / xDist)
        row = int((y - ulY) / yDist)
        return (column, row)
    
    def convertProjection(self, latlon, proj1, proj2):
        inProj = Proj(proj1)
        outProj = Proj(proj2)
        #x1,y1 = -11705274.6374,4826473.6922
        x2,y2 = transform(inProj,outProj, latlon[1], latlon[0])
        return x2, y2

    def pixel2coord(self, geoMatrix, x, y):
        """Returns global coordinates from pixel x, y coords
        Input: geoMatrix
               x - column number
               y - row number
        """
        xp = geoMatrix[1] * x + geoMatrix[2] * y + geoMatrix[0]
        yp = geoMatrix[4] * x + geoMatrix[5] * y + geoMatrix[3]
        return(xp, yp)
    
    def rossThick(self, sz, vz, ra):
        """
        Calculate the value of Ross-Thick (volumetric) kernel
        for the input angles- Solar Zenith, View Zenith and
        Relative Azimuth.
        Input angles are need to be in radians.
        The equations were adopted from MODIS BRDF/Albedo Product: Algorithm
        Theoretical Basis Document v 5.0
        """
        sz = np.abs(sz)
        vz = np.abs(vz)
        pa=np.arccos((np.cos(sz)*np.cos(vz))+(np.sin(sz)*np.sin(vz)*np.cos(ra))) #Phase Angle
        Kvol=(((((np.pi/2)-pa)*np.cos(pa))+np.sin(pa))/(np.cos(sz)+np.cos(vz)))-(np.pi/4) #Ross-Thick (volumetric) kernel
        return Kvol

    def liSparse(self, sz, vz, ra, br=1, hb=2):
        """
        Calculate the value of Li-Sparse (geometric) kernel
        for the input angles- Solar Zenith, View Zenith and
        Relative Azimuth.
        Input angles are need to be in radians.
        The equations were adopted from MODIS BRDF/Albedo Product: Algorithm
        Theoretical Basis Document v 5.0
        Optional parameters br and hb are the b/r and h/b ratios specified
        in the ATBD (page 14). They represent the crown shape and crown height
        respectively. The default values for these are those specified in
        the ATBD for the MODIS global processing.
        """
        sz = np.abs(sz)
        vz = np.abs(vz)
        sz1=np.arctan(br*np.tan(sz)) # Shape parameters(b/r)=1
        vz1=np.arctan(br*np.tan(vz)) # Shape parameters(b/r)=1
        pa1=np.arccos((np.cos(sz1)*np.cos(vz1))+(np.sin(sz1)*np.sin(vz1)*np.cos(ra)))
        D=np.sqrt((np.tan(sz1))**2+(np.tan(vz1))**2-(2*np.tan(sz1)*np.tan(vz1)*np.cos(ra)))
        cost=hb*((np.sqrt(D**2+(np.tan(sz1)*np.tan(vz1)*np.sin(ra))**2))/((1/np.cos(sz1))+(1/np.cos(vz1))))
        if np.isscalar(cost):
            if cost>1:
                cost=1
            if cost<-1:
                cost=-1
        else:
            cost[cost>1] = 1
            cost[cost<-1] = -1
        t=np.arccos(cost)
        O=1/np.pi*((t-(np.sin(t)*np.cos(t)))*((1/np.cos(sz1))+(1/np.cos(vz1))))
        Kgeo=O-(1/np.cos(sz1))-(1/np.cos(vz1))+(0.5*(1+np.cos(pa1))*(1/np.cos(sz1))*(1/np.cos(vz1))) #Li-Sparse (Geometric) kernel
        return Kgeo
    
    def calculateLST(self, b14, b15, soz, emis, emis_mask, f={'c':45.257935, 'a1':0.985361, 'a2':1.332220, 'a3':-41.750015, 'd':0.035390}):
        sozMean = np.mean(soz)
        secTheta = 1/math.cos(sozMean*np.pi/180) - 1
        lst = f['c'] + (f['a1']*b14)+ f['a2']*(b14 - b15) +f['a3']*emis + (f['d']*((b14 - b15)*secTheta))
        lstCelcius = lst - 273.15
        lstCelcius = np.array(lstCelcius)
        lstCelcius[emis_mask < 0] = 0
        return(lstCelcius)
        
        
    
