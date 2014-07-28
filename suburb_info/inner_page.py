__author__ = 'Han'

import requests
from bs4 import BeautifulSoup
import time
import random
import pymongo
from pymongo import MongoClient
data_client = MongoClient()
data_base = data_client.Locations
#add authenticate for the MongoDB
#data_base.authenticate('EZYProperty', '8jshf7asd')
super_c = data_base.suburb_info

header = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}

def get_detail_page(link):
    suburb = {}
    html = requests.get(link)
    dom = BeautifulSoup(html.content)
    for infoblock in dom.find_all("div", class_="pd-double-column"):
        if infoblock.find("div", class_="header").text == "Rent vs Own":
            details = infoblock.find("div", class_="pd-content-medium")
            for x in details.find_all('p'):
                title = x.b.text.replace(".", "")
                if len(title) != 0:
                    x.b.extract()
                clean_text = x.text.strip()
                suburb[title] = clean_text
    return suburb


url = "http://www.realestateview.com.au/propertydata/suburb-profile/victoria/"
html = requests.get(url, headers=header)
dom = BeautifulSoup(html.content)
alpha_list = dom.find("div", id="suburb_links")
list_a = []
s_counter = 0
e_counter = 0

for links in alpha_list.find_all("a"):
    print("Getting alpha list")
    list_a.append("http://www.realestateview.com.au"+links['href'])

#go through all the alpha lists
try:
    for urls in list_a:
        html_1 = requests.get(urls, headers=header)
        dom = BeautifulSoup(html_1.content)
        sub_list = {}
        time.sleep(1.5)
        list_suburb = dom.find("div", class_="pd-content-inner")
        for items in list_suburb.find_all("a"):
            sub_list[items.text] = "http://www.realestateview.com.au" + items['href']
        for detail_sub in sub_list.items():
            print("Process " + detail_sub[0])

            time.sleep(random.randint(1,5))
            details = get_detail_page(detail_sub[1])
            details['Suburb'] = detail_sub[0]
            results = super_c.insert(details)
            if results:
                s_counter += 1
                print("Done with %s"%detail_sub[0])
            else:
                e_counter += 1
                print("Error")
                print(results)
except:
    e_counter += 1
    print('Something wrong is happening :( Keep going')
    pass
print("All done with %d in total with %d errors"%(s_counter+e_counter, e_counter))
data_client.close()