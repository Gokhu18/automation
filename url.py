import pymongo
from pymongo import MongoClient

#connect to database
client = MongoClient('localhost',27017)
#set the db object to pricetracker database
db = client['pricetracker']
#set the db to TV collection
collection = db['TV']
#result = collection.find()
for doc in collection.find({}):
	# changed variable names
	print(doc['url'])
