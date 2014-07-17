__author__ = 'Han'

#aim to collect all the information from coles website and populate into database

import config
import requests
from bs4 import BeautifulSoup
import csv

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
writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='|')
writer.writerow(['Store Name','Address', 'Suburb','State', 'Post Code', 'Phone'])
for rows in states.find_all('div', class_='row'):
    bs = rows.find('a')
    if bs != None:
        counter += 1
        title = rows.a.div.h4.text
        pre_full_address = rows.find('span', class_='address').text
        full_address_list = pre_full_address.split(' ')
        post_code = full_address_list[-1]
        full_address_list.remove(post_code)
        land_info_results = suburb_database_check(post_code)
        error = 0
        suburb_name = ''
        state = ''
        for result in land_info_results:
            state = result['State']
            if full_address_list[-1] == result['Locality'].title():
                suburb_name = full_address_list[-1]
                del full_address_list[-1]
            else:
                if len(full_address_list) <= 2:
                    break
                else:
                    long_name = full_address_list[-1] + full_address_list[-2]
                    if long_name == result['Locality'].title():
                        suburb_name = long_name
                        del full_address_list[-1]
                        del full_address_list[-1]
                    else:
                        suburb_name = 'Unknown'
        full_address = (" ").join(full_address_list)
        phone = rows.find('span', class_='phone').text
        print('We are processing ' + title)
        writer.writerow([title, full_address, suburb_name, state, post_code, phone])

f.close()
print("Total valid record is %d"%counter)
config.data_base.logout()
config.data_client.close()

