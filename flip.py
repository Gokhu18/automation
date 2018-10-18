from selenium import webdriver
import pandas as pd
import time
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost',27017)
#set the db object to pricetracker database
db = client['pricetracker']
#set the db to TV collection
collection = db['TV']
driver = webdriver.Chrome()
for doc in collection.find({}):
	#storing the url in variable
	result = doc['url']
	driver.get(result)
	if (result != 'null'):
		try:
			for item in range(2,1,5):
				#Getting the price
				elem = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div['+item+']/div[1]/div/div[1]')
		except TypeError:
			print ("Some error in finding the price\t" + str(time.ctime()))
elem = pd.DataFrame(elem)
elem.to_csv('price.csv')