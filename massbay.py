# -*- coding: utf-8 -*-
"""
Created on Tue Apr 3 9:50:45 2018

@author: huimin
"""


import datetime as dt
import pytz
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pytz import timezone
import numpy as np
import csv
from scipy import  interpolate
from matplotlib.dates import date2num,num2date
from netCDF4 import Dataset
#from barycentric_polygonal_interpolation import get_drifter_track,get_fvcom,get_roms,calculate_SD,drifterhr
######## Hard codes ##########
st_lat=[]
st_lon=[]
latc=np.linspace(41.8,42.0,10)
lonc=np.linspace(-70.5,-70.2,10)

for aa in np.arange(len(lonc)):
    for bb in np.arange(len(latc)):
        st_lat.append(latc[bb])
        st_lon.append(lonc[aa])

###########################################################
urltime='''http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/archives/necofs_mb?time[0:1:34655]'''
ds = Dataset(urltime,'r').variables
######coastline#################
FN='necscoast_worldvec.dat'
CL=np.genfromtxt(FN,names=['lon','lat'])
###########save files to this folder################
filepath='files_20141118-25/'
days=7
start_time=dt.datetime(2014,11,18,0,0,0,0)

end_time=start_time+timedelta(hours=days*24)
index1=(start_time-datetime(1858,11,17,00,00,00)).days+(start_time-datetime(1858,11,17,00,00,00)).seconds/(60*60*24)
index2=(end_time-datetime(1858,11,17,00,00,00)).days+(end_time-datetime(1858,11,17,00,00,00)).seconds/(60*60*24)
ind1=np.argmin(abs(np.array(ds['time'])-index1))
ind2=np.argmin(abs(np.array(ds['time'])-index2))

lon=np.load('lonc.npy')#massbay model grid point
lat=np.load('latc.npy')#massbay model grid point

#############################################
urlroms = '''current_08hind_hourly.nc'''
dsroms = Dataset(urlroms,'r').variables

url1roms = '''gom6-grid.nc'''
ds1roms = Dataset(url1roms,'r').variables
lon_u=np.hstack(ds1roms['lon_u'][:])
lat_u=np.hstack(ds1roms['lat_u'][:])
lon_v=np.hstack(ds1roms['lon_v'][:])
lat_v=np.hstack(ds1roms['lat_v'][:])

##############################################3
url1='''http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/archives/necofs_mb?u[{0}:1:{1}][0][0:1:165094],v[{0}:1:{1}][0][0:1:165094]'''
url1 = url1.format(ind1, ind2)
ds1 = Dataset(url1,'r').variables
#########################################################
lonmassbay=[]
latmassbay=[]
timemassbay=[]
for a in np.arange(len(st_lon)):
    d=[]
    for b in np.arange(len(lon)):
        d.append((st_lon[a]-lon[b])*(st_lon[a]-lon[b])+(st_lat[a]-lat[b])*(st_lat[a]-lat[b]))
    index3=np.argmin(d)
    temlon=st_lon[a]
    temlat=st_lat[a]
    lonmass=[]
    latmass=[]
    timemass=[]
    '''
    lonmass.append(temlon)
    latmass.append(temlat)
    timemass.append(start_time)
    '''
    for c in np.arange(0,days*24+1):
        
        u_t=ds1['u'][c][0][index3]
        v_t=ds1['v'][c][0][index3]
        print 'a',a,'c',c,'time',start_time+timedelta(days=c/24.0),u_t,v_t
        
        dx = 60*60*u_t; dy = 60*60*v_t
        temlon = temlon + (dx/(111111*np.cos(temlat*np.pi/180)))
        temlat = temlat + dy/111111
        #######################################################
        d1=[]
        for dd in np.arange(len(lon_u)): 
            d1.append((lon_u[dd]-temlon)*(lon_u[dd]-temlon)+(lat_u[dd]-temlat)*(lat_u[dd]-temlat))
        index2roms=np.argmin(d1)
        
        d2=[]
        for b1 in np.arange(len(lon_v)): 
            d2.append((lon_v[b1]-temlon)*(lon_v[b1]-temlon)+(lat_v[b1]-temlat)*(lat_v[b1]-temlat))
        index3roms=np.argmin(d2)
        
        v0=np.hstack(dsroms['v'][0][-1][:][:])
        u0=np.hstack(dsroms['u'][0][-1][:][:])
        if v0[index3roms]>100000000 or u0[index2roms]>10000000000:
            print 'next'
            dis_coast=[]#all distances to coastline
            for i in range(len(CL)):
                dis=(temlon-CL['lon'][i])**2+(temlat-CL['lat'][i])**2
                dis_coast.append(dis)
            index_nearest=np.argmin(dis_coast)
            lonmass.append(CL['lon'][index_nearest])
            latmass.append(CL['lat'][index_nearest])
            timemass.append(start_time+timedelta(days=c/24.0))
            break
        else:
            lonmass.append(temlon)
            latmass.append(temlat)
            timemass.append(start_time+timedelta(days=c/24.0))
        #############################################3########
            ddd=[]
            for ba in np.arange(len(lon)):
                ddd.append((temlon-lon[ba])*(temlon-lon[ba])+(temlat-lat[ba])*(temlat-lat[ba]))
            index3=np.argmin(ddd)
            
    np.save(filepath+'lon%s'%str(a),lonmass)
    np.save(filepath+'lat%s'%str(a),latmass)
    np.save(filepath+'time%s'%str(a),timemass)
    lonmassbay.append(lonmass)
    latmassbay.append(latmass)
    timemassbay.append(timemass)

np.save(filepath+'lonmassbay',lonmassbay)
np.save(filepath+'latmassbay',latmassbay)
np.save(filepath+'timemassbay',timemassbay)
