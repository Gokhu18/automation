import requests
from bs4 import BeautifulSoup

def spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://www.amazon.in/s/ref=sr_pg_1?rh=n%3A976419031%2Ck%3ATV&page=' +str(page)+'&keywords=TV&ie=UTF8&qid=1539251022'
        source = (requests.get(url)).text
        obj = BeautifulSoup(source, "html5lib")
        # not the ideal way of getting links as these will get the link available in the webpage
        for link in obj.find_all('a'):
            # just getting all the links
            print(link.get('href'))
        page += 1
spider(2)
