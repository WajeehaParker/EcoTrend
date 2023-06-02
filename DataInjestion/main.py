import redis
import pandas as pd

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching and saving data ##########
WDI_data_1 = pd.read_csv('/app/Imports/WDIEXCEL_Data_part1.csv')
WDI_data_2 = pd.read_csv('/app/Imports/WDIEXCEL_Data_part2.csv')

columns_to_drop = list(range(1960, 2000))
columns_to_drop = [str(year) for year in columns_to_drop]
WDI_data_1 = WDI_data_1.drop(columns=columns_to_drop)
WDI_data_2 = WDI_data_2.drop(columns=columns_to_drop)

selected_countries=['AFE', 'CHN']

for index, row in WDI_data_1.iterrows():

    if(row['Country Code'] in selected_countries):
        country_code= row['Country Code']
        indicator_code= row['Indicator Code']

        for year in range(2000, 2021):
            key=f'{country_code}:{year}:{indicator_code}'
            value=str(row[str(year)])
            redis.set(key, value)

