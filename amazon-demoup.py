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
collection = db['updatedamazon']
logger.info('Using Collection')
#calling the webdriver
driver = webdriver.Chrome()
logger.info('Calling the Chrome webdriver')
#initializing different db
#conn = MongoClient('10.56.133.12',27017)
db1 = client['amazon']
col = db1['upprie']
logger.info('Connecting with database to store data')
dt = datetime.datetime.now().date()
logger.info('Setting the date')
#inserting the values into db
def inser(bar,model,price,review,rank):
	logger.info('Handling insertion')
	#({'brand':bar,'model':model,str(dt):{'price':price,'review':review}})
	db1.upprie.update_one({'Brand':bar,'Model':model},{"$set": {str(dt):{'Price':float(price),'Review':int(review),'Best Seller Rank':int(rank)}}},upsert = True)
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
			print("NO DATA")
			logger.error('No url is found')
			price = 0
		else:
			driver.get(result)
			logger.info('Iterating the webpages')
			try:
				price = str((driver.find_element_by_xpath('//*[@id="priceblock_ourprice" or @id="priceblock_saleprice" or @id="priceblock_dealprice"]')).text)
				logger.info('getting the price through xpaths')
				price = price.replace('   ','')
				price = price.replace(',','')
				print(price)
				logger.info('fetching price %s',price)
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
					review = review.replace(',','')
				else:
					review = driver.find_element_by_xpath('//*[@id="acrCustomerWriteReviewText"]')	
			except:
				logger.error("No element found in main loop", exc_info=True)
				pass
			print(review)
			logger.info('fetching No. of Reviews %s',review)
			try:
				rank = str(driver.find_element_by_xpath('//*[@id="SalesRank"]/td[2]/ul/li').text)
				# r = "in Electronics > Hi-Fi & Home Audio > Home Theater > Televisions"
				# rank = re.sub('\d','',r)
				rank = rank.replace(' in Electronics > Hi-Fi & Home Audio > Home Theater > Televisions > Smart Televisions','')
				rank = rank.replace('in Electronics > Hi-Fi & Home Audio > Home Theater > Televisions > Standard Televisions','')
				rank = rank.replace('in Electronics > Hi-Fi & Home Audio > Home Theater > Televisions','')
				rank = rank.replace('#','')
				print(rank)
				logger.info('Fetching Best Seller Rank %s',rank)
			except:
				rank = 0
			inser(bar,model,price,review,rank)
			logger.info('Calling the inser Function')
if __name__ == '__main__':
	main()
driver.quit()
logger.info('Quiting webpages')
print("Completed")
logger.info('All process completed')