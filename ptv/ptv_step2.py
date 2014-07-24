__author__ = 'Han'

__author__ = 'yuerzx'

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import csv
import time

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
filename = "bus" # tram or train or bus
f = open(filename +'_step1.csv', 'r', newline='')
fw = open(filename+ '_step2.csv', 'w', newline ='')
s_counter = 0
e_counter = 0
reader = csv.reader(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer = csv.writer(fw, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer.writerow(['S_Name','Suburb', 'lon', 'lat','link' ])
next(reader)
for row in reader:
    num = 0
    s_name  = row[0]
    suburb  = row[1]
    link    = row[2]
    html = None
    try:
        html = requests.get(link, headers=header, timeout = 3)
    except:
        try:
            html = requests.get(link, headers=header, timeout = 3)
        except:
            writer.writerow(['Error', suburb, 'Error', 'Error', link])
            e_counter += 1
            pass
        pass
    if html is not None:
        if html.status_code == 200:
            s_counter += 1
            detail_dom = BeautifulSoup(html.content)
            aside = detail_dom.find('div', class_="aside")
            print("We are processing %s"%suburb)
            num += 1
            for x in aside.findAll("li"):
                if x.text == "View on map":
                    geocode = x.a['href']
                    print(geocode)
                    geocode_list = geocode.split('=')[1].split(',')
                    lon = geocode_list[1]
                    lat = geocode_list[0]
                    writer.writerow([s_name, suburb,lon, lat, link])
            print("The number %d"%num)
    else:
        print('Unable to locate the files. ')
f.close()
fw.close()
print("We got %d in total with %d errors"%(s_counter,e_counter))
