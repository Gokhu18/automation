from lxml import html  
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep

def AmzonParser(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
	page = requests.get(url,headers=headers)
	while True:
		sleep(10)
		try:
			doc = html.fromstring(page.content)
			XPATH_NAME = '//*[@id="productTitle"]'
			XPATH_ORIGINAL_PRICE = '//*[@id="priceblock_dealprice"]'

			RAW_NAME = doc.xpath(XPATH_NAME)
			RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)

			NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
			ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None

			if page.status_code!=200:
				raise ValueError('captha')
			data = {
					'NAME':NAME,
					'ORIGINAL_PRICE':ORIGINAL_PRICE,
					'URL':url,
					}

			return data
		except Exception as e:
			print (e)

def ReadAsin():
	# AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
	AsinList = ['B0046UR4F4',
	'B00JGTVU5A',
	'B00GJYCIVK',
	'B00EPGK7CQ',
	'B00EPGKA4G',
	'B00YW5DLB4',
	'B00KGD0628',
	'B00O9A48N2',
	'B00O9A4MEW',
	'B00UZKG8QU',]
	extracted_data = []
	for i in AsinList:
		url = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=tv"+i
		print ("Processing: "+url)
		extracted_data.append(AmzonParser(url))
		sleep(10)
	f=open('data.json','w')
	json.dump(extracted_data,f,indent=4)


if __name__ == "__main__":
    ReadAsin()