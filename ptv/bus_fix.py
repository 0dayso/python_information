__author__ = 'Han'


__author__ = 'yuerzx'

import requests
from bs4 import BeautifulSoup
import csv

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
filename = "bus" # trams or trains
f = open(filename +'_step1_err.csv', 'r', newline='')
fw = open(filename+ '_step1_fix.csv', 'w', newline ='')
s_counter = 0
e_counter = 0
reader = csv.reader(f, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer = csv.writer(fw, delimiter=',',quoting=csv.QUOTE_NONE, quotechar='')
writer.writerow(['S_Name','suburb','link' ])
next(reader)
for row in reader:
    num = 0
    s_name  =   row[0]
    suburb  =   row[1]
    link    =   row[2]
    html    =   None
    if s_name == "Error":
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
    else:
        writer.writerow([s_name, suburb, link])
f.close()
fw.close()
print("We got %d in total with %d errors"%(s_counter,e_counter))