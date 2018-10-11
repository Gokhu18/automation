#!/usr/bin/env python
# -*- coding: utf-8 -*-	
from lxml import html  
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep

def ParseReviews(asin):
	# for i in range(5):
	# 	try:
	#This script has only been tested with Amazon.com
	amazon_url  = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=tv'+asin
	# Add some recent user agent to prevent amazon from blocking the request 
	# Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
	page = requests.get(amazon_url,headers = headers,verify=False)
	page_response = page.text

	parser = html.fromstring(page_response)
	XPATH_AGGREGATE = '//*[@id="acrCustomerReviewText"]'
	XPATH_REVIEW_SECTION_1 = '//*[@id="customer_review"]]'
	XPATH_REVIEW_SECTION_2 = '//*[@id="customer_review-R2S0AP10WVPKB6"]/div[2]/a[2]]'

	XPATH_AGGREGATE_RATING = '//*[@id="acrPopover"]/span[1]/a/i[1]/span'
	XPATH_PRODUCT_NAME = '//*[@id="productTitle"]'
	XPATH_PRODUCT_PRICE  = '//*[@id="priceblock_dealprice"]'
	
	raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
	product_price = ''.join(raw_product_price).replace(',','')

	raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
	product_name = ''.join(raw_product_name).strip()
	total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
	reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
	if not reviews:
		reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
	ratings_dict = {}
	reviews_list = []
	
	if not reviews:
		raise ValueError('unable to find reviews in page')

	#grabing the rating  section in product page
	for ratings in total_ratings:
		extracted_rating = ratings.xpath('./td//a//text()')
		if extracted_rating:
			rating_key = extracted_rating[0] 
			raw_rating_value = extracted_rating[1]
			rating_value = raw_rating_value
			if rating_key:
				ratings_dict.update({rating_key:rating_value})
	
	#Parsing individual reviews
	for review in reviews:
		XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
		XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
		XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
		XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
		XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
		XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
		XPATH_AUTHOR  = './/span[contains(@class,"profile-name")]//text()'
		XPATH_REVIEW_TEXT_3  = './/div[contains(@id,"dpReviews")]/div/text()'
		
		raw_review_author = review.xpath(XPATH_AUTHOR)
		raw_review_rating = review.xpath(XPATH_RATING)
		raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
		raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
		raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
		raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
		raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

		#cleaning data
		author = ' '.join(' '.join(raw_review_author).split())
		review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
		review_header = ' '.join(' '.join(raw_review_header).split())

		try:
			review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
		except:
			review_posted_date = None
		review_text = ' '.join(' '.join(raw_review_text1).split())

		#grabbing hidden comments if present
		if raw_review_text2:
			json_loaded_review_data = json.loads(raw_review_text2[0])
			json_loaded_review_data_text = json_loaded_review_data['rest']
			cleaned_json_loaded_review_data_text = re.sub('<.*?>','',json_loaded_review_data_text)
			full_review_text = review_text+cleaned_json_loaded_review_data_text
		else:
			full_review_text = review_text
		if not raw_review_text1:
			full_review_text = ' '.join(' '.join(raw_review_text3).split())

		raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
		review_comments = ''.join(raw_review_comments)
		review_comments = re.sub('[A-Za-z]','',review_comments).strip()
		review_dict = {
							'review_comment_count':review_comments,
							'review_text':full_review_text,
							'review_posted_date':review_posted_date,
							'review_header':review_header,
							'review_rating':review_rating,
							'review_author':author

						}
		reviews_list.append(review_dict)

	data = {
				'ratings':ratings_dict,
				'reviews':reviews_list,
				'url':amazon_url,
				'price':product_price,
				'name':product_name
			}
	return data
	 #	except ValueError:
 	#	print("Retrying to get the correct response")

	 #return {"error":"failed to process the page","asin":asin}
			
def ReadAsin():
	#Add your own ASINs here 
	AsinList = ['B01INGAGE2','B01ICVLKFC','B071CTX49P']
	extracted_data = []
	for asin in AsinList:
		print("Downloading and processing page https://www.amazon.in/"+asin)
		extracted_data.append(ParseReviews(asin))
		sleep(10)
	f = open('data.json','w')
	json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()