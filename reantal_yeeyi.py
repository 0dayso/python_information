__author__ = 'yuerzx'
from bs4 import BeautifulSoup
import requests
import pre_process
import random
import time

#Basic setting area
#start page
home_url = "http://www.yeeyi.com/bbs/house.php?mod=list&filter=all&city=30&sortid=1&page="

#hide the system as a chrome

#Get the first few pages of yeeyi
import config
print("Program is ready to go :)")
available_links = {}
for x in range(1, 10):
    home_url_tmp = home_url + str(x)
    print("Get page " + str(x) + " Ready!")
    home_html = requests.get(home_url_tmp, headers = config.header)
    print(home_url_tmp)
    home_index = BeautifulSoup(home_html.content, from_encoding="gbk")
    available_links.update(pre_process.front_page_links(home_index))

rental = {}
counter = 0
total = 0
for md5, link in available_links.items():
    total += 1
    counter += 1
    rental_id = pre_process.rental_collection.insert({"md5": md5})
    rental[rental_id] = {}
    rental[rental_id]["url"] = link
    time.sleep(random.randrange(1,3))
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
        total += 1
        result = pre_process.rental_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
        if result:
            print("入库成功: " + str(rental[ids]['title']))
    rental = {}


print("Total valid record is" + total)
pre_process.rental_client.close()