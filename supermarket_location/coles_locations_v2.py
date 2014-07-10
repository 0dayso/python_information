__author__ = 'Han'

#As the google maps is not offering the most accurate points, we need to get it from the pre setting points by myself


import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import re

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
html = requests.get('http://www.coles.com.au/store-locator', headers= header)
dom = BeautifulSoup(html.content)
states = dom.find('section', class_='states')
counter = 0

def geo_details(link):
    details_link = 'http://www.coles.com.au' + link
    for i in range(0,2):
        detail_page = requests.get(details_link, headers=header)
        Error = 1
        if detail_page.status_code == 200:
            Error = 0
            detail_dom = BeautifulSoup(detail_page.content)
            script_section = detail_dom.find('section', class_="row store-detail")
            script = script_section.find('script', text=True)
            jsonValue = '[%s]' % (script.text.split('[', 1)[1].rsplit(']', 1)[0],)
            value = json.loads(jsonValue)
            store_number = store_info_select(link)
            store_value = {}
            for x in value:
                if x['Id'] == store_number:
                    store_value = x
        else:
            print('Error in system')
            location['Latitude'] = 'Error'
            location['Longitude'] = 'Error'
            location['Id'] = store_info_select(link)
        if Error == 0:
            break
    return store_value

def store_info_select(link):
    item = re.search('\d{1,6}', link)
    item_number = item.group(0)
    return item_number

#close up the documents for csv
f = open('coles.csv', 'w', newline='')
writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer.writerow(['S_Id','S_Name', 'Suburb','State', 'PCode', 'Phone', 'lat', 'lng', 'Full_Address', 'link'])
for rows in states.find_all('div', class_='row'):
    bs = rows.find('a')
    break_point = False
    if bs != None:
        counter += 1
        locality            = ''
        state               = ''
        post_code           = ''
        lat, lng, store_id ='','',''
        store_name = rows.a.div.h4.text
        locality = rows.a['title']
        details_link_pre = rows.a['href']
        state = details_link_pre.split('/')[-2].upper()
        pre_full_address = rows.find('span', class_='address').text
        post_code = pre_full_address.split(' ')[-1]
        phone = rows.find('span', class_='phone').text
        location = geo_details(details_link_pre)
        if location:
            lat = location['Latitude']
            lng = location['Longitude']
            store_id = location['Id']
        print('We are processing ' + store_name)
        writer.writerow([store_id, store_name, locality, state, post_code, phone, lat, lng, pre_full_address, details_link_pre])
        #google is only allowed for 10 requests per second
        time.sleep(0.3)
    if break_point == True:
        break
f.close()
print("Total valid record is %d"%counter)


