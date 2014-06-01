__author__ = 'yuerzx'
from bs4 import BeautifulSoup
import requests
import pre_process

#Basic setting area
#start page
home_url = "http://www.yeeyi.com/bbs/house.php?mod=list&filter=all&city=30&sortid=1&page="

#hide the system as a chrome
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
#Get the first few pages of yeeyi
for x in range(1, 2):
    home_url = home_url + str(x)
    home_html = requests.get(home_url, headers = header)
    home_index = BeautifulSoup(home_html.content, from_encoding="gbk")
    available_links = pre_process.front_page_links(home_index)
rental = {}
counter = 0
for md5, link in available_links.items():
    counter += 1
    rental_id = pre_process.rental_collection.insert({"md5": md5})
    rental[rental_id] = {}
    rental[rental_id]["url"] = link
    html = requests.get(link, headers=header)
    index = BeautifulSoup(html.content,from_encoding='GBK')
    #Get the publishing data
    rental[rental_id]["publish_time"] = pre_process.get_publish_time(index)
    #Get the title
    rental[rental_id]["title"] = pre_process.get_page_title(index)
    #Prepare all the documents content
    page_content = index.find('td', class_='t_f')
    pre_process.cleanup_marks(page_content)
    items = pre_process.information_pickup(page_content)
    for k, v in items.items():
        rental[rental_id][k] = v
    if counter == 5:
        for ids, keys in rental.items():
            result = pre_process.rental_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
            if result:
                print("入库成功: " + str(rental[ids]['title']))
        counter = 0
        rental = {} #clean up the dict to save memory

while rental:
    for ids, keys in rental.items():
            result = pre_process.rental_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
            if result:
                print("入库成功: " + str(rental[ids]['title']))
    rental = {}

print(rental)
