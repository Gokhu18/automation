import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
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
#result = collection.find()
for doc in collection.find({}):
	# changed variable names
	print(doc['url'])

#Getting the time for the creation
print (time.ctime())
driver = webdriver.Chrome()
#Saving data to a excelsheet
wb = Workbook()
ws = wb.create_sheet("Sheet1",0)
wb.save("price.xlsx")

#Total value there in db
for val in range(1,254):
	val = str(val)
	xfile = openpyxl.load_workbook('price.xlsx')
	sheet = xfile.get_sheet_by_name('Sheet1')
	driver.get(obj['url'])
	if(url == '1'):
		#Click on the url(Kindly Say me from where to find the url)
		driver.find_title_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/h1/span').click()
		try:
			#Getting the title of the content
			title = driver.find_title_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/h1/span')
		except Exception:
			print ("No link to find title\t") + str(time.ctime())
			time.sleep(20)
			driver.refresh()
			time.sleep(5)
		try:
			#Getting the price
			price = driver.find_price_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]')
		except Exception:
			print ("Some error in finding the price\t") + str(time.ctime())
			pass
		try:
			if(len(title.text)>1):
				print (r)
				ws.cell(row = r, column = 0).value = title.text
				ws.cell(row = r, column = 1).value = price.text
				# worksheet.write(row,col,title.text)
				# worksheet.write(row,col+1,price.text)
			
				url += 1
				print ("post increment") + str(r)
				wb.save('price.xlsx')

			else:
				print ("Some problem here at row: ") +str(row) + str(time.ctime())
		except Exception:
			pass
	print ("Data Scraped from url: ")+val
driver.quit()
print ("Completed") 
print (time.ctime())