import redis
import csv

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

########## fetching data from redis ##########

value = redis.get("AFE:2020:EG.ELC.ACCS.RU.ZS")
print(value)
