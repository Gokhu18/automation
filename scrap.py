import selenium
from selenium import webdriver
from selenium.common.exceptions import *
import time, openpyxl
from openpyxl import Workbook
import pymongo
from pymongo import MongoClient

#connect to database
client = MongoClient('localhost',27017)
#set the db object to pricetracker database
db = client['pricetracker']
#set the db to TV collection
collection = db['TV']
driver = webdriver.Chrome()
for doc in collection.find({}):
	# changed variable names
	result = doc['url']
	if( len(result) == 0):
		print("NO DATA")
	else:
		driver.get(result)
		price = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[3 or 4]/div[1]/div/div[1]')
		print(price.text)
		
	#	try:
	#		for item in range(2,1,5):
	#			#Getting the price
	#			price = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div['+item+']/div[1]/div/div[1]')
	#			print(price.text)
	#	except Exception as er:
	#		print(er)

	print ("Data Scraped from url: ")
driver.quit()
print ("Completed") 
print (time.ctime())