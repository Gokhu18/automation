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
logger.info('Connected to local server')
#set the db object to pricetracker database
db = client['pricetracker']
logger.info('Selecting the database')
#set the db to TV collection
collection = db['amazon']
logger.info('Using Collection')
#calling the webdriver
driver = webdriver.Chrome()
logger.info('Calling the Chrome webdriver')
#initializing different db
conn = MongoClient('10.56.133.12',27017)
logger.info('Connecting with remote server')
db1 = conn['test_review']
col = db1['amazon']
logger.info('Connecting with the database')
dt = datetime.datetime.now().date()
logger.info('Setting the date')
#inserting the values into db
def inser(bar,model,price,review):
	logger.info('Handling insertion')
	({'brand':bar,'model':model,str(dt):{'price':price,'review':review}})
	logger.info('Inserting the data into collection of db')
	db1.amazon.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'price':price,'review':review}}},upsert = True)
	logger.info('Updating the database')
	print("Insert Complete")
	logger.info('Insertion Done')
#defining main function
def main():
	for doc in collection.find({}):
		logger.info('find all the data from doc')
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
			print("NO DATA")
			logger.error('No url is found', result)
		else:
			driver.get(result)
			logger.info('Loading webpages')
			try:
				price = str((driver.find_element_by_xpath('//*[@id="priceblock_ourprice" or @id="priceblock_saleprice" or @id="priceblock_dealprice"]')).text)
				price = price.replace('   ','')
				print(price)
				logger.info('fetching price %s',price)
				logger.info('getting the price through xpaths')
			except:
				price = 0
			try:
				review = 0
				if(review == 0):
					review = driver.find_element_by_xpath('//*[@id="cmrs-atf" or @id="acrCustomerReviewText"]').text
					review = review.replace('customer reviews','')
					review = review.replace('customer review','')
					review = review.replace('Bethefirsttoreviewthisitem','0')
					review = review.replace(' ','')
					logger.info('fetching No. of Ratings and Reviews %s',review)
				else:
					review = driver.find_element_by_xpath('//*[@id="acrCustomerWriteReviewText"]')		
			except:
				logger.error("No element found in main loop", exc_info=True)
				logger.info('No Review or Ratings found')
				pass
			print(review)
			inser(bar,model,price,review)
			logger.info('Calling the inser Function')
if __name__ == '__main__':
	main()
driver.quit()
logger.info('Quiting webpages')
print("Completed")
logger.info('All process completed')