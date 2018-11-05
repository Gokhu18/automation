import selenium
from selenium import webdriver
import pymongo,datetime,re
from pymongo import MongoClient
from log_controller import *
log_info("Selecting collection")

#connect to database
logger.info('Connected to local server')
client = MongoClient('localhost',27017)
#set the db object to pricetracker database
logger.info('Selecting the database')
db = client['pricetracker']
#set the db to TV collection
logger.info('Using Collection')
collection = db['flipkart']
#calling the webdriver
logger.info('Calling the Chrome webdriver')
driver = webdriver.Chrome()
#initializing different db
logger.info('Connecting with remote server')
conn = MongoClient('10.56.133.12',27017)
logger.info('Connecting with the database')
db1 = conn['test_review']
col = db1['flipkart']
logger.info('Setting the date')
dt = datetime.datetime.now().date()

#inserting the values into db
def inser(bar,model,price,rating,review):
	logger.info('Handling insertion')
	({'brand':bar,'model':model,str(dt):{'price':price,'rating':rating,'review':review}})
	logger.info('Inserting the data into collection')
	db1.flipkart.update_one({'brand':bar,'model':model}, {"$set": {str(dt):{'price':price,'rating':rating,'review':review}}},upsert = True)
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
			price = str((driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[3 or 4]/div[1]/div/div[1]')).text)
			price = price.replace('Price: Not Available','0')
			logger.info('fetching price %s',price)
			logger.info('getting the price through xpaths')
			try:
				rating = 0
				review = 0
				if(rating == 0 and 
					review == 0):
					rating = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[2]/div/div/span[2]/span/span[1]').text
					rating = rating.replace(' Ratings ','')
					review = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[2]/div/div/span[2]/span/span[3]').text
					review = review.replace(' Reviews','')
					review = review.replace(' ','')
				else:
					rating = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span[1]')
					review = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span[1]')
					logger.info('fetching No. of Ratings and Reviews %s',rating,review)
			except:
				logger.error("No review found in main loop", exc_info=True)
				pass
				print("No element found")
				logger.info('No Review or Ratings found')
			inser(bar,model,price,rating,review)
			logger.info('Calling the inser Function')

if __name__ == '__main__':
	main()
driver.quit()
logger.info('Quiting webpages')
print("Completed")
logger.info('All process completed')