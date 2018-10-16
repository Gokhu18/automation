import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
for doc in collection.find({}):
	# changed variable names
	result = print(doc['url'])
	driver = webdriver.Chrome()
	#Saving data to a excelsheet
	wb = Workbook()
	ws = wb.create_sheet("Sheet1",0)
	wb.save("price.xlsx")
	#Total value there in database
	val = doc('result')
	xfile = openpyxl.load_workbook('price.xlsx')
	sheet = xfile.get_sheet_by_name('Sheet1')
	driver.get('result')
	if (val):
		try:
			#Getting the price
			price = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]')
		except Exception:
			print ("Some error in finding the price\t") + str(time.ctime())
			pass
			wb.save('price.xlsx')
		else:
			print ("Some problem here at row: ") +str(row) + str(time.ctime())
	print ("Data Scraped from url: ")+val
driver.quit()
print ("Completed") 
print (time.ctime())