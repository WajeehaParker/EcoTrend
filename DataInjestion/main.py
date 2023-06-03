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

########## inserting data in redis ##########

selected_indicators=['EG.ELC.ACCS.RU.ZS', 'EG.ELC.ACCS.RU.ZS']

for index, row in WDI_data.iterrows():

    if(row['Indicator Code'] in selected_indicators):
        country_code= row['Country Code']
        indicator_code= row['Indicator Code']

        for year in range(2000, 2021):
            key=f'{country_code}:{year}:{indicator_code}'
            value=str(row[str(year)])
            redis.set(key, value)

print("fetching data")
print(redis.get("AFE:2020:EG.ELC.ACCS.RU.ZS"))
print(redis.get("USA:2020:EG.ELC.ACCS.RU.ZS"))
