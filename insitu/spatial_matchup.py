#%%
import numpy as np
import pandas as pd
import netCDF4 as nc


#%%
#location
gfile = "D:\\Data\\GK2_GC2\\GK2B_GOCI2_L2_20220101_031530_LA_S007_AC.nc"
ds = nc.Dataset(gfile)
glat = ds['navigation_data']['latitude'][:]
glon = ds['navigation_data']['longitude'][:]

pfile = "D:\\koem\\CSV_koem.csv"
insitu = pd.read_csv(pfile)
insitu_name = insitu['정점명']
insitu_lat = insitu['위도']
insitu_lon = insitu['경도']

for i in range(0, len(insitu)):
    _lat = insitu_lat.loc[i]
    _lon = insitu_lon.loc[i]
    dis = ((glat-_lat)**2 + (glon-_lon)**2)**(1/2)
    _idx = np.where(dis == np.min(dis))


#%%
#

df = pd.read_csv("koem 관측자료.csv")
date = df['관측일자']
yy = date
mm = date
dd = date

path = "\\10.108.0.221\realtime_g2gs"