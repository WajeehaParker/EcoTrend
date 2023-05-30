import redis
import csv

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching data from redis ##########

value = redis.get('mykey')
print(value)
vehicles = redis.zrange('vehicles', 0, -1)
print(vehicles)
