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
#Saving data to a excelsheet
wb = Workbook()
ws = wb.create_sheet("Sheet1",0)
sheet = wb.active
rows = sheet.rows
driver = webdriver.Chrome()
for doc in collection.find({}):
	# changed variable names
	result = doc['url']
	#Total value there in database
	xfile = openpyxl.load_workbook('price.xlsx')
	sheet = xfile.get_sheet_by_name('Sheet1')
	driver.get(result)
	if (result != 'null'):
		try:
			for item in range(2,1,5):
				#Getting the price
				price = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div['+item+']/div[1]/div/div[1]')
		except TypeError:
			print ("Some error in finding the price\t" + str(rows) + str(time.ctime()))
			continue
		else:
			print ("Some problem here at db: " + str(time.ctime()))
	print ("Data Scraped from url: ")
sheet.title = 'Data'
sheet.append(price)
wb.save('price.xlsx')	
driver.quit()
print ("Completed") 
print (time.ctime())