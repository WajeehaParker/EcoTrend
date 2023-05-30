import redis
import csv

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching and saving data ##########


"""with open("../DataSets/Education/Literacy_rate_among_adults_aged_15 years_in_percent.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row)

file_path = "../DataSets/Education/Literacy_rate_among_adults_aged_15 years_in_percent.csv"
du_literacyRate = pd.read_csv(file_path)

print(edu_literacyRate)
print("before loop")

for index, row in edu_literacyRate.iterrows():
    print("inside loop")
    redis.set(f"Country:{index}", row['Country or Area'])
    redis.set(f"Year:{index}", row['Year(s)'])
    redis.set(f"literacy_rate:{index}", row['Value'])

for index, row in edu_literacyRate.iterrows():
    country_value = redis.get(f"Country:{index}")
    year_value = redis.get(f"Year:{index}")
    literacy_rate_value = redis.get(f"literacy_rate:{index}")
    print(country_value)
    print(year_value)
    print(literacy_rate_value)"""



########## end fetching and saving data ##########


redis.set('mykey', 'Hello from Python!')
value = redis.get('mykey')
print(value)

redis.zadd('vehicles', {'car' : 0})
redis.zadd('vehicles', {'bike' : 0})
vehicles = redis.zrange('vehicles', 0, -1)
print(vehicles)
