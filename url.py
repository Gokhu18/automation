import pymongo
from pymongo import MongoClient

#connect to database
client = MongoClient('localhost',27017)
#set the db object to pricetracker database
db = client.pricetracker
db = client[pricetracker]
#set the db to TV collection
collection = db.TV
collection = db[TV]
#result = collection.find()
for str in collection.findAll():
	print (str[url])
