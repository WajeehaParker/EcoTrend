import redis
import pandas as pd

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching data from csv ##########
WDI_data_1 = pd.read_csv('/app/Imports/WDIEXCEL_Data_part1.csv')
WDI_data_2 = pd.read_csv('/app/Imports/WDIEXCEL_Data_part2.csv')

########## concat as 1 dataframe ##########
WDI_data = pd.concat([WDI_data_1, WDI_data_2], axis=0)
WDI_data = WDI_data.reset_index(drop=True)

########## dropping unnecessary columns ##########
columns_to_drop = list(range(1960, 2000))
columns_to_drop = [str(year) for year in columns_to_drop]
WDI_data = WDI_data.drop(columns=columns_to_drop)

print(WDI_data.shape)

########## replacing null values by the average ##########
for column in WDI_data.columns:
    if WDI_data[column].isnull().any():
        mean_value = WDI_data[column].mean()
        WDI_data[column].fillna(mean_value, inplace=True)

########## inserting values in redis (key starting with Values) ##########

selected_indicators=['SP.POP.TOTL', 'SP.POP.TOTL.FE.IN' 'SP.POP.TOTL.MA.IN', 'SP.DYN.CBRT.IN', 'SP.DYN.CDRT.IN', 'SP.DYN.LE00.IN', 
                     'SP.POP.GROW', 'IQ.CPA.GNDR.XQ', 'SH.XPD.CHEX.GD.ZS', 'SL.EMP.1524.SP.NE.ZS', 'SE.ADT.LITR.ZS', 'EG.ELC.ACCS.ZS',
                     'SL.UEM.TOTL.NE.ZS', 'SL.UEM.1524.NE.ZS', 'NY.ADJ.NNTY.KD.ZG', 'FM.LBL.BMNY.GD.ZS', 'GC.DOD.TOTL.GD.ZS',
                     'GC.DOD.TOTL.CN', 'BN.CAB.XOKA.GD.ZS', 'GC.XPN.TOTL.GD.ZS', 'GC.XPN.TOTL.CN', 'EG.USE.COMM.FO.ZS', 'NY.GDP.MKTP.KD.ZG',
                     'GC.TAX.TOTL.GD.ZS', 'NY.GNS.ICTR.ZS', 'FP.CPI.TOTL.ZG', 'NY.GSR.NFCY.CD', 'NY.ADJ.AEDU.CD', 'SE.SEC.UNER.LO.ZS',
                     'SL.TLF.0714.ZS', 'SE.PRM.UNER.ZS', 'SE.COM.DURS', 'SE.TER.CUAT.BA.ZS', 'SE.XPD.TOTL.GD.ZS', 'BN.CAB.XOKA.CD',
                     'BX.GSR.ROYL.CD', 'BM.GSR.ROYL.CD', 'BX.GSR.TOTL.CD', 'BX.KLT.DINV.CD.WD', 'BX.GRT.EXTA.CD.WD', 'BM.GSR.TOTL.CD',
                     'BM.GSR.NFSV.CD', 'BX.GRT.TECH.CD.WD', 'DT.DOD.DECT.CD', 'NY.GDP.MKTP.CD', 'NY.GDP.PCAP.CD', 'FI.RES.TOTL.CD',
                     'GC.REV.XGRT.GD.ZS', 'BX.TRF.PWKR.CD.DT']

for index, row in WDI_data.iterrows():

    if(row['Indicator Code'] in selected_indicators):
        country_code= row['Country Code']
        indicator_code= row['Indicator Code']

        for year in range(2000, 2021):
            key=f'Values:{country_code}:{year}:{indicator_code}'
            value=str(row[str(year)])
            redis.set(key, value)


########## inserting indicators in redis (key starting with Indicators) ##########
indicator_codes = WDI_data['Indicator Code'].unique()
indicator_names = WDI_data['Indicator Name'].unique()

for code, name in zip(indicator_codes, indicator_names):
    if(code in selected_indicators):
        redis.set(f'Indicator:{code}', name)

print(redis.get("Indicator:SP.POP.TOTL"))

########## inserting countries in redis (key starting with Countries) ##########
indicator_codes = WDI_data['Country Code'].unique()
indicator_names = WDI_data['Country Name'].unique()

for code, name in zip(indicator_codes, indicator_names):
    redis.set(f'Countries:{code}', name)

print(redis.get("Countries:USA"))

