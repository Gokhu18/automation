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
#set the db object to pricetracker database
db = client['pricetracker']
#set the db to TV collection
collection = db['amznsoundbar']
#calling the webdriver
driver = webdriver.Chrome()
#initializing different db
#conn = MongoClient('10.56.133.12',27017)
db1 = client['amazon']
col = db1['soundbar']
dt = datetime.datetime.now().date()
#inserting the values into db
def inser(bar,model,price,review):
	({'brand':bar,'model':model,str(dt):{'price':price,'review':review}})
	db1.soundbar.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'price':float(price),'review':int(review)}}},upsert = True)
	print("Insert Complete")
#defining main function
def main():
	for doc in collection.find({}):
		# storing the url
		result = doc['url']
		#storing the brandname
		bar = doc['brand']
		#storing the model name
		model = doc['model']
		if( len(result) == 0):
			print("NO DATA")
		else:
			driver.get(result)
			try:
				price = str((driver.find_element_by_xpath('//*[@id="priceblock_ourprice" or @id="priceblock_saleprice" or @id="priceblock_dealprice"]')).text)
				price = price.replace('   ','')
				price = price.replace(',','')
				print(price)
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
			inser(bar,model,price,review)
if __name__ == '__main__':
	main()
driver.quit()
print("Completed")