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
def inser(bar,model,price,review,reviews):
	({'brand':bar,'model':model,str(dt):{'price':price,'review':review,'reviews':reviews}})
	db1.soundbar.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'price':price,'review':review,'reviews':reviews}}},upsert = True)
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
			# use class instead of xpaths
			# print(review1)
			try:
				price = str((driver.find_element_by_xpath('//*[@id="priceblock_ourprice" or @id="priceblock_saleprice" or @id="priceblock_dealprice"]')).text)
				price = price.replace('   ','')	
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
				else:
					review = driver.find_element_by_xpath('//*[@id="acrCustomerWriteReviewText"]')		
			except:
				logger.error("No element found in main loop", exc_info=True)
				pass
			print(review)
			revie = 0
			if(revie != 0):
				revie = driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div[2]/a')
				revie.click()
			asin = str((driver.find_element_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]')).text)
			for p_no in range(1,10):
				driver.get('https://www.amazon.in/product-reviews/'+asin+'/ref=cm_cr_getr_d_paging_btm_'+str(p_no)+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(p_no)+'')
				rs = driver.find_elements_by_class_name('review-text')
				for r in rs:
					print(r.text)
					reviews = r.text
					inser(bar,model,price,review,reviews)
if __name__ == '__main__':
	main()
driver.quit()
print("Completed")
