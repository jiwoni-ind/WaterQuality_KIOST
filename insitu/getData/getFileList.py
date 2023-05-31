#%%
import pandas as pd
import netCDF4 as nc
import numpy as np

#%%
df1 = pd.read_csv("D:\\koem\\insitu_koem_2021_2022.csv", encoding='CP949')
df2 = pd.read_csv("E:\\Work\\CSV_koem.csv")
df = pd.merge(df2, df1, on=['정점명'])
iname = df['정점명']
idate = df['조사일자']
ilat = df['위도']
ilon = df['경도']

root = 'D:\\Data\\GK2_GC2\\'
# var = ['Chl', 'CDOM', 'TSS', 'IOP']
gval = []


#%%
for i in range(0, len(df)):
    # print(i)
    # _name = iname.loc[i]
    _date = idate.loc[i]
    _lat = ilat.loc[i]
    _lon = ilon.loc[i]

    yy = _date.split("-")[0]
    mm = _date.split("-")[1]
    dd = _date.split("-")[2]
    path = root + yy + '\\' + mm + '\\'
    # GK2B_GOCI2_L2_20220216_031530_LA_S007_AC.nc
    # fname = 'GK2B_GOCI2_L2_' + yy + mm + dd + \
    #     '_031530_LA_S007_AC.nc' 
    chl_fname = 'GK2B_GOCI2_L2_' + yy + mm + dd + \
                '_031530_LA_S007_Chl.nc' 
    cdom_fname = 'GK2B_GOCI2_L2_' + yy + mm + dd + \
                '_031530_LA_S007_CDOM.nc'
    tss_fname = 'GK2B_GOCI2_L2_' + yy + mm + dd + \
            '_031530_LA_S007_TSS.nc'
    iop_fname = 'GK2B_GOCI2_L2_' + yy + mm + dd + \
            '_031530_LA_S007_IOP.nc'
    
    try:
        # ds = nc.Dataset(path + fname)
        chl_ds = nc.Dataset(path + 'Chl\\' + chl_fname)
        cdom_ds = nc.Dataset(path + 'CDOM\\' + cdom_fname)
        tss_ds = nc.Dataset(path + 'TSS\\' + tss_fname)
        iop_ds = nc.Dataset(path + 'IOP\\' + iop_fname)

        glat = chl_ds['navigation_data']['latitude'][:]
        glon = chl_ds['navigation_data']['longitude'][:]
        dis = ((glat-_lat)**2 + (glon-_lon)**2)**(1.0/2)
        _idx = np.where(dis == np.min(dis))
        
        # Rrs380 = ds['geophysical_data']['Rrs']['Rrs_380'][_idx].data
        # Rrs412 = ds['geophysical_data']['Rrs']['Rrs_412'][_idx].data
        # Rrs443 = ds['geophysical_data']['Rrs']['Rrs_443'][_idx].data
        # Rrs490 = ds['geophysical_data']['Rrs']['Rrs_490'][_idx].data
        # Rrs510 = ds['geophysical_data']['Rrs']['Rrs_510'][_idx].data
        # Rrs555 = ds['geophysical_data']['Rrs']['Rrs_555'][_idx].data
        # Rrs620 = ds['geophysical_data']['Rrs']['Rrs_620'][_idx].data
        # Rrs660 = ds['geophysical_data']['Rrs']['Rrs_660'][_idx].data
        # Rrs680 = ds['geophysical_data']['Rrs']['Rrs_680'][_idx].data
        # Rrs709 = ds['geophysical_data']['Rrs']['Rrs_709'][_idx].data
        # Rrs745 = ds['geophysical_data']['Rrs']['Rrs_745'][_idx].data
        # Rrs865 = ds['geophysical_data']['Rrs']['Rrs_865'][_idx].data
        # tmp = [Rrs380[0][0], Rrs412[0][0], Rrs443[0][0], Rrs490[0][0], 
        #     Rrs510[0][0], Rrs555[0][0], Rrs620[0][0], Rrs660[0][0], 
        #     Rrs680[0][0], Rrs709[0][0], Rrs745[0][0], Rrs865[0][0]]
        chl = chl_ds['geophysical_data']['Chl'][_idx].data
        cdom = cdom_ds['geophysical_data']['CDOM'][_idx].data
        tss = tss_ds['geophysical_data']['TSS'][_idx].data

        adg443 = iop_ds['geophysical_data']['a_dg_443'][_idx].data
        achl443 = iop_ds['geophysical_data']['a_chl_443'][_idx].data
        bbp555 = iop_ds['geophysical_data']['bb_p_555'][_idx].data

        atot380 = iop_ds['geophysical_data']['a_total']['a_total_380'][_idx].data
        atot412 = iop_ds['geophysical_data']['a_total']['a_total_412'][_idx].data
        atot443 = iop_ds['geophysical_data']['a_total']['a_total_443'][_idx].data
        atot490 = iop_ds['geophysical_data']['a_total']['a_total_490'][_idx].data
        atot510 = iop_ds['geophysical_data']['a_total']['a_total_510'][_idx].data
        atot555 = iop_ds['geophysical_data']['a_total']['a_total_555'][_idx].data
        atot620 = iop_ds['geophysical_data']['a_total']['a_total_620'][_idx].data
        atot660 = iop_ds['geophysical_data']['a_total']['a_total_660'][_idx].data
        atot680 = iop_ds['geophysical_data']['a_total']['a_total_680'][_idx].data
        atot709 = iop_ds['geophysical_data']['a_total']['a_total_709'][_idx].data
        atot745 = iop_ds['geophysical_data']['a_total']['a_total_745'][_idx].data
        atot865 = iop_ds['geophysical_data']['a_total']['a_total_865'][_idx].data
        
        bbtot380 = iop_ds['geophysical_data']['bb_total']['bb_total_380'][_idx].data
        bbtot412 = iop_ds['geophysical_data']['bb_total']['bb_total_412'][_idx].data
        bbtot443 = iop_ds['geophysical_data']['bb_total']['bb_total_443'][_idx].data
        bbtot490 = iop_ds['geophysical_data']['bb_total']['bb_total_490'][_idx].data
        bbtot510 = iop_ds['geophysical_data']['bb_total']['bb_total_510'][_idx].data
        bbtot555 = iop_ds['geophysical_data']['bb_total']['bb_total_555'][_idx].data
        bbtot620 = iop_ds['geophysical_data']['bb_total']['bb_total_620'][_idx].data
        bbtot660 = iop_ds['geophysical_data']['bb_total']['bb_total_660'][_idx].data
        bbtot680 = iop_ds['geophysical_data']['bb_total']['bb_total_680'][_idx].data
        bbtot709 = iop_ds['geophysical_data']['bb_total']['bb_total_709'][_idx].data
        bbtot745 = iop_ds['geophysical_data']['bb_total']['bb_total_745'][_idx].data
        bbtot865 = iop_ds['geophysical_data']['bb_total']['bb_total_865'][_idx].data

        tmp = [chl[0][0], cdom[0][0], tss[0][0], adg443[0][0], achl443[0][0], 
               bbp555[0][0], atot380[0][0], atot412[0][0], atot443[0][0], 
               atot490[0][0], atot510[0][0], atot555[0][0], atot620[0][0], 
               atot660[0][0], atot680[0][0], atot709[0][0], atot745[0][0], 
               atot865[0][0], bbtot380[0][0], bbtot412[0][0], bbtot443[0][0], 
               bbtot490[0][0], bbtot510[0][0], bbtot555[0][0], bbtot620[0][0], 
               bbtot660[0][0], bbtot680[0][0], bbtot709[0][0], bbtot745[0][0], 
               bbtot865[0][0]]
        gval.append(tmp)
        tmp = []
        print(str(i)+'/'+str(len(df)))

    except FileNotFoundError:
        tmp = [-999.0, -999.0, -999.0, -999.0, 
            -999.0, -999.0, -999.0, -999.0, 
            -999.0, -999.0, -999.0, -999.0]
        gval.append(tmp)
        tmp = []
        print(str(i)+'/'+str(len(df))+'--> FileNotFound')

#%%
_gval = pd.DataFrame(gval)
cols = ["Chl", "CDOM", "TSS", "adg443", "achl443", "bbp555", "atot380", 
        "atot412", "atot443", "atot490", "atot510", "atot555", "atot620", 
        "atot660", "atot680", "atot709", "atot745", "atot865", "bbtot380", 
        "bbtot412", "bbtot443", "bbtot490", "bbtot510", "bbtot555", "bbtot620", 
        "bbtot660", "bbtot680", "bbtot709", "bbtot745", "bbtot865"]
_gval.columns = cols
out = pd.concat([df, _gval], axis=1)
out.to_csv("E:\\Work\\koem_gc2_matchup_2021_2022_standard.csv", index=False, encoding='utf-8')



# %%
