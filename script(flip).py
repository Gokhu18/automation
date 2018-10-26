import selenium
from selenium import webdriver
import pymongo,datetime
from pymongo import MongoClient
from log_controller import *
log_info("Selecting collection")

#connect to database
logger.info('Connect to local database')
client = MongoClient('localhost',27017)
#set the db object to pricetracker database
logger.info('Selecting the database')
db = client['pricetracker']
#set the db to TV collection
logger.info('Using Collection')
collection = db['TV']
#calling the webdriver
logger.info('Calling the Chrome webdriver')
driver = webdriver.Chrome()
#initializing different db
logger.info('Connecting with remote database')
conn = MongoClient('10.56.133.12',27017)
db1 = conn['pricetracker']
col = db1['pricetracker']
logger.info('Setting the date')
dt = datetime.datetime.now().date()

#inserting the values into db
def inser(bar,model,price):
	logger.info('Handling insertion')
	doc1 = ({'brand':bar,'model':model,str(dt):price})
	logger.info('Storing in doc1 %s',doc1)
	if(doc1 == None):
		logger.info('No documents found')
		col.insert_one(doc1)
		logger.info('Inserting the doc1 into collection')
	else:
		db1.pricetracker.update_one({'model':model}, {"$set": {str(dt):price}},upsert = True)
		logger.info('Updating the database')
	print("Insert Complete")
	logger.info('Insertion Done')
#defining main function
def main():
	for doc in collection.find({}):
		logger.debug('%s doc',doc)
		# storing the url
		result = doc['url']
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
			logger.info('Iterating the webpages')
			price = (driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[3 or 4]/div[1]/div/div[1]').text)
			logger.debug('fetching price %s'price,)
			logger.info('getting the price through xpaths')
			inser(bar,model,price)
			logger.info('Calling the inser Function')

if __name__ == '__main__':
	main()

driver.quit()
logger.info('Quiting webpages')
print("Completed")
logger.info('All process completed')