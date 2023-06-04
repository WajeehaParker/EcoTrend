from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
import redis
import pandas as pd

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

for key in keys:
    # Split the key into its components
    components = key.decode().split(':')
    country_codes.append(components[1])
    years.append(components[2])
    indicator_codes.append(components[3])
    country_names.append(redis.get(f'Countries:{components[1]}'))
    indicator_names.append(redis.get(f'Indicator:{components[3]}'))

    value = redis.get(key).decode()
    values.append(value)

########## creating dataframe ##########
data = {
    'Country_Name': country_names,
    'Country_Code': country_codes,
    'Indicator_Name': indicator_names,
    'Indicator_Code': indicator_codes,
    'Year': years,
    'Value': values
}
df = pd.DataFrame(data)

print(df)


"""
# Create a SparkSession
spark = SparkSession.builder.appName("LinearRegression").getOrCreate()

# Load the data
data = spark.read.csv("/app/sparkml/data.csv", header=True, inferSchema=True)

# Prepare the data for training
assembler = VectorAssembler(inputCols=["x"], outputCol="features")
data = assembler.transform(data)

# Split the data into training and test sets
trainData, testData = data.randomSplit([0.7, 0.3], seed=123)

# Create a LinearRegression model
lr = LinearRegression(featuresCol="features", labelCol="y")

# Train the model
model = lr.fit(trainData)

# Make predictions on the test set
predictions = model.transform(testData)

# Show the predicted values
predictions.select("x", "y", "prediction").show()

# Stop the SparkSession
spark.stop()

"""
