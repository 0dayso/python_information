import requests
from bs4 import BeautifulSoup
import csv
# same structure but different address. Easy!!:)
html = requests.get("http://ptv.vic.gov.au/getting-around/stations-and-stops/metropolitan-buses/")
dom = BeautifulSoup(html.content)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
a_list = dom.find("div", id="alpha-list")
f = open('buses.csv', 'w', newline='')
writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE, quotechar='')
writer.writerow(['Suburb', 'link'])
address_list = {}
s_counter = 0
e_counter = 0
details_in_link = ""
for x in a_list.findAll("li"):
    details_link = x.a['href']
    surburb = x.a.text
    s_counter += 1
    print("We are processing %s" % surburb)
    writer.writerow([surburb, details_link])

print("We got %d in total" % s_counter)

