import pymongo
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['price2']
col = db['TV']
for doc in col.find({}):
	br = doc['brand']
	md = doc['model']
	dt1 = doc['2018-10-23']
	dt2 = doc['2018-10-24']
	re = br,md,dt1,dt2

conn = MongoClient('10.56.133.12',27017)
db1 = conn['pricetracker']
coll = db1['pricetracker']
for doc in col.find({}):
	br = doc['brand']
	md = doc['model']
	dt1 = doc['2018-10-23']
	dt2 = doc['2018-10-24']
	doc1 = ({'brand':br,'model':md,'2018-10-23':dt1,'2018-10-24':dt2})
	coll.insert_one(doc1)

