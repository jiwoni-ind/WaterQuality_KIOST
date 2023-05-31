#%%
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pandas as pd

sdate = 20210101
edate = 20230301
service_key = 'qPwOeIrU-2303-JKEKOQ-0541'

url = f'https://www.nifs.go.kr/OpenAPI_xml?id=femoSeaList&key={service_key}'\
    f'&sdate={sdate}&edate={edate}'

#%%
result = urlopen(url)  #7
house = BeautifulSoup(result, 'lxml-xml')  #8
te = house.find_all('item')  #9

# %%
datas = []  #1

for i in range(len(te)):  #2
    pname = te[i].FISHERY.string.strip()  
    pnumber = te[i].LOCATION_POINT.text.strip()
    lat = te[i].LATITUDE.string.strip()
    lon = te[i].LONGITUDE.string.strip()
    YY = te[i].DATE_Y.string.strip()
    MM = te[i].DATE_M.string.strip()
    DD = te[i].DATE_D.string.strip()
    hh = te[i].TIME_H.string.strip()
    mm = te[i].TIME_I.string.strip()
    depth = te[i].DEPTH.text.strip()
    temp = te[i].TEMP_S.text.strip()
    sal = te[i].SAL_S.text.strip()
    pH = te[i].PH_S.text.strip()
    DO = te[i].DO_S.text.strip()
    COD = te[i].COD_S.text.strip()
    NH4_N = te[i].NH4_N_S.text.strip()
    NO3_N = te[i].NO3_N_S.text.strip()
    NO2_N = te[i].NO2_N_S.text.strip()
    DIN = te[i].DIN_S.text.strip()
    TN = te[i].TN_S.text.strip()
    DIP = te[i].DIP_S.text.strip()
    TP = te[i].TP_S.text.strip()
    SIL = te[i].SIL_S.text.strip()
    CHL = te[i].CHL_S.text.strip()
    SS = te[i].SS_S.text.strip()
    trans = te[i].M.text.strip()
        
    data = [pname, pnumber, lat, lon, YY, MM, DD, hh, mm, depth, temp, sal, pH, DO, COD, NH4_N, NO3_N, NO2_N, DIN, TN,
            DIP, TP, SIL, CHL, SS, trans]  #3
    datas.append(data)  #4
# %%
df = pd.DataFrame(datas, columns=['pname', "pnumber", "lat", "lon", "YY", "MM", "DD", "hh", "mm", "depth", "temp", "sal", 
                                "pH", "DO", "COD", "NH4_N", "NO3_N", "NO2_N", "DIN", "TN", "DIP", "TP", "SIL", "CHL", "SS", "trans"])

df.to_csv('D://nifs//fishery_data.csv', sep=',', index=False, encoding='CP949')