import selenium
from selenium import webdriver
import pymongo,datetime
from pymongo import MongoClient

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
def inser(bar,model,price):
	doc = ({'brand':bar,'model':model,str(dt):price})
	if(doc == None):
		col.insert_one(doc)
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
			price = (driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[3 or 4]/div[1]/div/div[1]').text)
			inser(bar,model,price)
if __name__ == '__main__':
	main()
driver.quit()
print("Completed")