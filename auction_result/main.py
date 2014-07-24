__author__ = 'Han'

import requests
from bs4 import BeautifulSoup
import time
import datetime
import config

auctions = {}
link = 'http://www.realestateview.com.au/propertydata/auction-results/victoria/'
home_html = requests.get(link, headers = config.header)
auction_data = BeautifulSoup(home_html.content)
auctions['overall']={}
auctions['house']={}
auctions['apartment']={}

publish_time_pre = auction_data.find('div', class_="pd-content-heading-inner")
publish_time = publish_time_pre.text.split('-')

import re
def solve(s):
    return re.sub(r'(\d)(st|nd|rd|th|TH|ST|ND|RD)', r'\1', s)

full_start_time = publish_time[1] + " 2014"
full_end_time   = publish_time[2] + " 2014"
start_time = datetime.datetime.strptime(solve(full_start_time),"%A %d %B %Y")
end_time   = datetime.datetime.strptime(solve(full_start_time),"%A %d %B %Y")

print(start_time, end_time)

for x in auction_data.findAll("div", class_="pd-column-wrapper"):
    if x.find("h1") and x.find("h1").text =="vic Auction Results":
        auctions['overall']['WCR'] = x.find("div", class_="pd-content-medium-inner").span.text
        auctions['overall']['WRA'] = x.find("div", style= "float: right; width: 48%; text-align: center; line-height: 1;").span.text
