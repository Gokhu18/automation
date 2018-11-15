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
collection = db['sdbar']
#calling the webdriver
driver = webdriver.Chrome()
#initializing different db
db1 = client['flip']
col = db1['sndbar']
dt = datetime.datetime.now().date()
#inserting the values into db
def inser(bar,model,price,rating,review,review1,review2,review3):
	({'brand':bar,'model':model,str(dt):{'price':price,'rating':rating,'review':review,'review1':review1,'review2':review2,'review3':review3}})
	#if(doc1 == None):
	#	col.insert_one(doc1)
	#else:
	db1.sndbar.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'price':price,'rating':rating,'review':review,'review1':review1,'review2':review2,'review3':review3}}},upsert = True)
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
			price = (str((driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2 or 3]/div/div[3 or 4]/div[1]/div/div[1]')).text))
			price = price.replace('Price: Not Available','0')
			try:
				review1 = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[6]/div[3 or 4 or 5 or 6]/div/div[3 or 4]/div[1]/div/div/div[2]/div/div/div').text
				review2 = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[6]/div[3 or 4 or 5 or 6]/div/div[3 or 4]/div[2]/div/div/div[2]/div/div/div').text
				review3 = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[6]/div[3 or 4 or 5 or 6]/div/div[3 or 4]/div[3]/div/div/div[2]/div/div/div').text
				#review4 = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[6]/div[3 or 4 or 5 or 6]/div/div[3 or 4]/div[4]/div/div/div[2]/div/div/div').text
			except:
				review1 = 0
				review2 = 0
				review3 = 0	
				#review4 = 0
			print(price)
			print(review1)
			print(review2)
			print(review3)
			#print(review4)
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
			except:
				logger.error("No element found in main loop", exc_info=True)
				pass
				print("No element found")	
			print(rating)
			print(review)
			inser(bar,model,price,rating,review,review1,review2,review3)
if __name__ == '__main__':
	main()
driver.quit()
print("Completed")