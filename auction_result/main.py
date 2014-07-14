__author__ = 'Han'

import requests
from bs4 import BeautifulSoup
import timestring
import config

auctions = {}
link = 'http://www.realestateview.com.au/propertydata/auction-results/victoria/'
home_html = requests.get(link, headers = config.header)
auction_data = BeautifulSoup(home_html.content)
auctions['overall']={}
auctions['house']={}
auctions['apartment']={}
auctions['land']={}

publish_time_pre = auction_data.find('div', class_="pd-content-heading-inner")
publish_time = publish_time_pre.text.split('-')

