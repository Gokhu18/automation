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
collection = db['TV']
#calling the webdriver
driver = webdriver.Chrome()
#initializing different db
db1 = client['price']
col = db1['TV']
dt = datetime.datetime.now().date()
#inserting the values into db
def inser(bar,model,price,review,rating):
	doc1 = ({'brand':bar,'model':model,str(dt):price})
	if(doc1 == None):
		col.insert_one(doc1)
	else:
		db1.TV.update_one({'model':model}, {"$set": {str(dt):price}},upsert = True)
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
			price = str((driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[3 or 4]/div[1]/div/div[1]')).text)
			price = price.replace('Price: Not Available','0')
			try:
				rating = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[1]').text
				rating = rating.replace(' Ratings ','')
				review = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]').text
				review = review.replace('Reviews','')
			except NoSuchElementException:
				pass
				print("No element found")
				
			print(review)
			print(rating)
			inser(bar,model,price,review,rating)

if __name__ == '__main__':
	main()
driver.quit()
print("Completed")