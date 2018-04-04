# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 17:15:29 2018

@author: huimin
"""

import numpy as np
import matplotlib.pyplot as plt

st_lat=[]
st_lon=[]
latc=np.linspace(41.8,42.0,10)
lonc=np.linspace(-70.5,-70.2,10)

for aa in np.arange(len(lonc)):
    for bb in np.arange(len(latc)):
        st_lat.append(latc[bb])
        st_lon.append(lonc[aa])
 
FN='necscoast_worldvec.dat'
CL=np.genfromtxt(FN,names=['lon','lat'])
fig,ax=plt.subplots(1,1,figsize=(8,8))#sharex=True,sharey=True,dpi=800,figsize=(15,15))
plt.subplots_adjust(wspace=0.1,hspace=0.1)
ax.plot(CL['lon'],CL['lat'],'b-')
       
lons=np.load('lonmassbay.npy')
lats=np.load('latmassbay.npy')
times=np.load('timemassbay.npy')

for i in range(len(lons)):
    ax.scatter(st_lon[i],st_lat[i],color='green')
    ax.scatter(lons[i][-1],lats[i][-1],color='red')
    ax.plot(lons[i][:],lats[i][:],'y-')
    
ax.set_xlim([-70.7,-69.9])
ax.set_ylim([41.5,42.1])
plt.savefig('particle_tracking_massbay',dpi=200)
plt.show()