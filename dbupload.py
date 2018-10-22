
# This program will be used to read data from the sheet and uploaded to the database with a proper schema
import xlrd, re, pymongo
from pymongo import MongoClient

def upload(brand, model, size, smart,url):
	client = MongoClient('localhost',27017)
	db = client['pricetracker']
	collection = db['TV']
	doc = ({"brand":brand,"model":model,"size":size,"smart":smart,"url":url})
	collection.insert(doc)

def read(fn):
	# loading the sheet onto the memory
	workbook = xlrd.open_workbook(fn)
	# loading the first sheet from the workbook
	worksheet = workbook.sheet_by_index(0)
	for val in range(1,worksheet.nrows):
		brand = (worksheet.cell(val,0).value)
		model = (worksheet.cell(val,1).value)
		size = (worksheet.cell(val,2).value)
		smart = (worksheet.cell(val,3).value)
		url  = (worksheet.cell(val,4).value)
		print(brand)
		print(model)
		print(size)
		print(smart)
		print(url)
		upload(brand, model, size, smart,url)
	# print("Program upload complete")

def main():
	# enter the name of the sheet
	fn = 'C:\\Users/sauravkhandelwal/Documents/GitHub/links.xlsx'
	# calling the read functin responsible
	read(fn)

if __name__ == '__main__':
	main()
