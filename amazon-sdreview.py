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
col = db1['sbreview']
dt = datetime.datetime.now().date()
#inserting the values into db
def inser(bar,model,noofreview,reviews):
	#doc1 = ({'brand':bar,'model':model,str(dt):{'noofreview':noofreview,'reviews':reviews}})
	#col.insert_one(doc1)
	db1.sbreview.update_one({'brand':bar,'model':model},{"$set": {str(dt):{'noofreview':noofreview,'reviews':reviews}}},upsert = True)
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
			asin = str((driver.find_element_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]')).text)
			for p_no in range(1,9):
				driver.get('https://www.amazon.in/product-reviews/'+asin+'/ref=cm_cr_getr_d_paging_btm_'+str(p_no)+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(p_no)+'')
				noofreview = str(driver.find_element_by_xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span').text)
				print(noofreview)
				try:
					#rn = str(driver.find_element_by_xpath('//a[@data-hook="profile-name"]').text)
					rt = str(driver.find_element_by_xpath('//a[@data-hook="review-title"]').text)
					rd = str(driver.find_element_by_xpath('//span[@data-hook="review-date"]').text)
					rb = str(driver.find_element_by_xpath('//span[@data-hook="review-body"]').text)
					for r in rt,rd,rb:
						reviews = r
						print(reviews)
						inser(bar,model,noofreview,reviews)	
				except:
					print("No more reviews")
					break
						
if __name__ == '__main__':
	main()
driver.quit()
print("Completed")