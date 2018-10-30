 
# This program will be used to read data from the sheet and uploaded to the database with a proper schema
import xlrd, re, pymongo
from pymongo import MongoClient

def upload(brand, product, model, hyperlink):
	client = MongoClient('localhost',27017)
	db = client['pricetracker']
	collection = db['amazon']
	doc = ({"brand":brand,"product":product,"model":model,"hyperlink":hyperlink})
	collection.insert(doc)

def read(fn):
	# loading the sheet onto the memory
	workbook = xlrd.open_workbook(fn)
	# loading the first sheet from the workbook
	worksheet = workbook.sheet_by_index(0)
	for val in range(1,worksheet.nrows):
		brand = (worksheet.cell(val,0).value)
		product = (worksheet.cell(val,1).value)
		model = (worksheet.cell(val,2).value)
		hyperlink = (worksheet.cell(val,3).value)
		print(brand)
		print(product)
		print(model)
		print(hyperlink)
		upload(brand, product, model, hyperlink)
	# print("Program upload complete")

def main():
	# enter the name of the sheet
	fn = 'C:\\Users/sauravkhandelwal/Desktop/Scraper/URLs_AMAZON.xlsx'
	# calling the read functin responsible
	read(fn)

if __name__ == '__main__':
	main()
