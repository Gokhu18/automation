import selenium
from selenium import webdriver
from selenium.common.exceptions import *
import pymongo,datetime
import re
from pymongo import MongoClient
from log_controller import *
log_info("Selecting collection")

#connect to database
client = MongoClient('localhost',27017)
logger.info('Connect to local database')
#set the db object to pricetracker database
db = client['pricetracker']
logger.info('Selecting the database')
#set the db to TV collection
collection = db['updatedflipkart']
logger.info('Using Collection')
#calling the webdriver
driver = webdriver.Chrome()
logger.info('Calling the Chrome webdriver')
#initializing different db
db1 = client['flip']
col = db1['pricerev']
logger.info('Connecting with database to store data')
dt = datetime.datetime.now().date()
logger.info('Setting the date')
#inserting the values into db
def inser(bar,model,price,rating,review):
	logger.info('Handling insertion')
	#({'brand':bar,'model':model,str(dt):{'price':price,'rating':rating,'review':review}})
	#if(doc1 == None):
	#	col.insert_one(doc1)
	#else:
	db1.pricerev.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'price':int(price),'rating':int(rating),'review':int(review)}}},upsert = True)
	logger.info('Inserting and Updating the database')
	print("Insert Complete")
#defining main function
def main():
	for doc in collection.find({}):
		logger.info('finding data in collection')
		# storing the url
		result = doc['hyperlink']
		logger.info('parsing the Url into variable result')
		#storing the brandname
		bar = doc['brand']
		logger.info('parsing the brand into variable bar')
		#storing the model name
		model = doc['model']
		logger.info('parsing the model into variable model')
		if( len(result) == 0):
			price = 0
			print("NO DATA")
			logger.error('No url is found', result)
		else:
			driver.get(result)
			logger.info('Iterating the webpages')
			try:
				price = (str((driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[3 or 4]/div[1]/div/div[1]')).text))
				logger.info('getting the price through xpaths')
				price = price.replace('Price: Not Available','0')
				price = price.replace('₹','')
				price = price.replace(',','')
				price = price.replace('Check\nEnter pincode','0')
				print(price)
				logger.info('fetching price %s',price)
			except:
				price = 0
			try:
				rating = 0
				review = 0
				if(rating == 0 and 
					review == 0):
					rating = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[2]/div/div/span[2]/span/span[1]').text
					rating = rating.replace(' Ratings ','')
					rating = rating.replace(',','')
					review = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[2]/div/div/span[2]/span/span[3]').text
					review = review.replace(' Reviews','')
					review = review.replace(' ','')
					review = review.replace(',','')
				else:
					rating = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span[1]')
					review = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span[1]')
			except:
				logger.error("No element found in main loop", exc_info=True)
				pass
				print("No element found")	
			print(rating)
			logger.info('Fetching No. of Ratings %s',rating)
			print(review)
			logger.info('Fetching No. of Reviews %s',review)
			inser(bar,model,price,rating,review)
			logger.info('Calling the inser Function')
if __name__ == '__main__':
	main()
driver.quit()
logger.info('Quiting webpages')
print("Completed")
logger.info('All process completed')