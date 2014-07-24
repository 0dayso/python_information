__author__ = 'yuerzx'

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import csv
import time

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
filename = "bus" # trams or trains
f = open(filename +'.csv', 'r', newline='')
fw = open(filename+ '_step1.csv', 'w', newline ='')
s_counter = 0 
e_counter = 0
reader = csv.reader(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer = csv.writer(fw, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer.writerow(['S_Name','suburb','link' ])
next(reader)
for row in reader:
    suburb = row[0]
    link = row[1]
    html = None
    try:
        html = requests.get(link, headers=header, timeout = 3)
    except:
        try:
            html = requests.get(link, headers=header, timeout = 3)
        except:
            writer.writerow(['Error', suburb, link])
            e_counter += 1
            pass
        pass
    if html is not None:
        if html.status_code == 200:
            s_counter += 1
            detail_dom = BeautifulSoup(html.content)
            stop_list = detail_dom.find('div', id="content")
            print("We are processing %s"%suburb)
            num = 0
            for x in stop_list.findAll("li"):
                num += 1
                details_name = x.a.text
                details_in_link = x.a['href']
                writer.writerow([details_name, suburb, details_in_link])
                print("The number %d"%num)
    else:
        print('Unable to locate files!')
f.close()
fw.close()
print("We got %d in total with %d errors"%(s_counter,e_counter))