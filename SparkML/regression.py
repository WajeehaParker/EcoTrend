from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression, GBTRegressor, RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from sklearn.ensemble import GradientBoostingRegressor
import redis
import pandas as pd
import pickle
import os
import subprocess
import shutil

print("inside SparkML")
pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching data from redis ##########

keys = redis.keys('Values:*')
country_codes = []
country_names = []
years = []
indicator_codes = []
indicator_names = []
values = []

selected_countries=['BGD', 'PAK', 'PRK', 'CHN', 'USA', 'ARE', 'IND', 'JPN']
selected_indicators=['SP.POP.TOTL', 'SP.POP.TOTL.FE.IN' 'SP.POP.TOTL.MA.IN', 'SP.DYN.CBRT.IN', 'SP.DYN.CDRT.IN', 'SP.DYN.LE00.IN', 
                     'SP.POP.GROW', 'IQ.CPA.GNDR.XQ', 'SH.XPD.CHEX.GD.ZS', 'SL.EMP.1524.SP.NE.ZS', 'SE.ADT.LITR.ZS', 'EG.ELC.ACCS.ZS',
                     'SL.UEM.TOTL.NE.ZS', 'SL.UEM.1524.NE.ZS', 'NY.ADJ.NNTY.KD.ZG', 'FM.LBL.BMNY.GD.ZS', 'GC.DOD.TOTL.GD.ZS',
                     'GC.DOD.TOTL.CN', 'BN.CAB.XOKA.GD.ZS', 'GC.XPN.TOTL.GD.ZS', 'GC.XPN.TOTL.CN', 'EG.USE.COMM.FO.ZS', 'NY.GDP.MKTP.KD.ZG',
                     'GC.TAX.TOTL.GD.ZS', 'NY.GNS.ICTR.ZS', 'FP.CPI.TOTL.ZG', 'NY.GSR.NFCY.CD', 'NY.ADJ.AEDU.CD', 'SE.SEC.UNER.LO.ZS',
                     'SL.TLF.0714.ZS', 'SE.PRM.UNER.ZS', 'SE.COM.DURS', 'SE.TER.CUAT.BA.ZS', 'SE.XPD.TOTL.GD.ZS', 'BN.CAB.XOKA.CD',
                     'BX.GSR.ROYL.CD', 'BM.GSR.ROYL.CD', 'BX.GSR.TOTL.CD', 'BX.KLT.DINV.CD.WD', 'BX.GRT.EXTA.CD.WD', 'BM.GSR.TOTL.CD',
                     'BM.GSR.NFSV.CD', 'BX.GRT.TECH.CD.WD', 'DT.DOD.DECT.CD', 'NY.GDP.MKTP.CD', 'NY.GDP.PCAP.CD', 'FI.RES.TOTL.CD',
                     'GC.REV.XGRT.GD.ZS', 'BX.TRF.PWKR.CD.DT']

for key in keys:
    # Split the key into its components
    components = key.decode().split(':')
    if(components[1] in selected_countries):
        country_codes.append(components[1])
        years.append(components[2])
        indicator_codes.append(components[3])
        country_names.append(redis.get(f'Countries:{components[1]}'))
        indicator_names.append(redis.get(f'Indicator:{components[3]}'))
        
        value = redis.get(key).decode()
        values.append(value)

########## creating dataframe ##########
data = {
    'Country Name': country_names,
    'Country Code': country_codes,
    'Indicator Name': indicator_names,
    'Indicator Code': indicator_codes,
    'Year': years,
    'Value': values
}
df = pd.DataFrame(data)

print(df)

########## Encoding ##########

"""
dft = df.drop(df.index[1:])
dft['Country Name']="United States"
dft['Country Code']="USA"
dft['Indicator Code']="NY.ADJ.NNTY.KD.ZG"
dft['Indicator Name']="Adjusted net national income (annual % growth)"
dft['Year']="2019"
"""

X = df.drop(columns=['Country Name', 'Indicator Name'])
X['Indicator Code'] = X['Indicator Code'].replace(selected_indicators, range(len(selected_indicators)))
X['Country Code'] = X['Country Code'].replace(selected_countries, range(len(selected_countries)))
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(0)
X = X.astype(int)
X=X.astype(int)
y = pd.to_numeric(df['Value'], errors='coerce')

print(X)

"""
Xt=dft.drop(columns=['Country Name', 'Indicator Name'])
Xt['Indicator Code'] = Xt['Indicator Code'].replace(selected_indicators, range(len(selected_indicators)))
Xt['Country Code'] = Xt['Country Code'].replace(selected_countries, range(len(selected_countries)))
Xt=Xt.astype(int)

print(Xt)
"""

########## Applying Machine Learning Techniques ##########

spark = SparkSession.builder.appName("Regression").getOrCreate()
inputCols=['Country Code', 'Indicator Code', 'Year']
outputCol='Value'

assembler = VectorAssembler(inputCols=inputCols, outputCol="features")
df_spark = spark.createDataFrame(X)
df_transformed = assembler.transform(df_spark)

trainData, testData = df_transformed.randomSplit([0.7, 0.3], seed=123)

print("Gradient Boosting")
model = GBTRegressor(featuresCol="features", labelCol=outputCol).fit(trainData)
predictions = model.transform(testData)
#predictions.select("features", outputCol, "prediction").show()
predictions.select("features", "prediction").show()

"""
print(X)
print(y)
"""
########## Generating pickle object for streamlit ##########

#X = df.drop(columns=['Value'])
feature_vectors = df_transformed.select('features').collect()
feature_list = [row.features.toArray() for row in feature_vectors]
X = pd.DataFrame(feature_list, columns=['Country Code', 'Indicator Code', 'Year'])

"""
print("dataframe for pickle")
print(X)
"""

reg=GradientBoostingRegressor().fit(X,y)
pickle_model = {
    'model': reg,
    'X':X
}

pickle.dump(pickle_model, open('ecoTrend_model.sav', 'wb'))
local_directory = os.getcwd()
local_file_path = os.path.join(local_directory, 'ecoTrend_model.sav')

destination_directory = 'D:/IBA/EcoTrend/Visualization'
os.makedirs(destination_directory, exist_ok=True)
destination_file_path = os.path.join(destination_directory, 'model.sav')
shutil.copy2(local_file_path, destination_directory)

"""
print(local_directory)
command = f"ls {local_directory}"
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

output = result.stdout.decode('utf-8')
error = result.stderr.decode('utf-8')

print("Output:", output)
print("Error:", error)
"""