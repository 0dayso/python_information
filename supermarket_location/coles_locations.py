__author__ = 'Han'

#aim to collect all the information from coles website and populate into database

import config
import requests
from bs4 import BeautifulSoup
import csv
import google_maps_api
import time

html = requests.get('http://www.coles.com.au/store-locator', headers= config.header)
dom = BeautifulSoup(html.content)
states = dom.find('section', class_='states')
counter = 0
post_code_database = config.data_base.postcode

def suburb_database_check(post_code):
    #search the post code from database and find the way to match suburb and states
    search_result = post_code_database.find({"Pcode":int(post_code)}, {'Pcode':1, 'Locality':1,'State':1 })
    return search_result


#close up the documents for csv
f = open('D:\playground\coles.csv', 'w', newline='')
writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
#writer.writerow(['Store Name','S_No','S_name', 'Suburb','State', 'PCode', 'Phone', 'lat', 'lng', 'Full_Address'])
for rows in states.find_all('div', class_='row'):
    bs = rows.find('a')
    break_point = False
    if bs != None:
        counter += 1
        store_name = rows.a.div.h4.text
        pre_full_address = rows.find('span', class_='address').text
        location = google_maps_api.google_decode(pre_full_address)
        street_number       = ''
        street_name         = ''
        locality            = ''
        state               = ''
        post_code           = ''
        if location['status'] != 'OK':
            print('Something wrong with google maps and we are going to stop now!!')
            print(location)
            break_point = True
            break
        else:
            lat                 = location['results'][0]['geometry']['location']['lat']
            lng                 = location['results'][0]['geometry']['location']['lng']
            location_components = location['results'][0]['address_components']
            for items in location_components:
                for type in items['types']:
                    if type == 'street_number':
                        street_number = items['short_name']
                    elif type == 'route':
                        street_name = items['short_name']
                    elif type == 'locality':
                        locality = items['short_name']
                    elif type == 'administrative_area_level_1':
                        state = items['short_name']
                    elif type == 'postal_code':
                        post_code = items['short_name']
                    elif type == 'establishment':
                        street_name = items['short_name']
        phone = rows.find('span', class_='phone').text
        print('We are processing ' + store_name)
        writer.writerow([store_name, street_number,street_name, locality, state, post_code, phone, lat, lng, pre_full_address])
        #google is only allowed for 10 requests per second
        time.sleep(1)
    if counter == 10 or break_point == True:
        break
f.close()
print("Total valid record is %d"%counter)
config.data_base.logout()
config.data_client.close()

