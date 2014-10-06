

__author__ = 'yuerzx'

import requests
from bs4 import BeautifulSoup
import hashlib
import config
import time
import random

articles = {}
domain = 'www.xkb.com.au'
link = 'http://xkb.com.au/html/caifu/dichantouzi/'
counter = 0
#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()
#Get ready for the database
news_collection = config.data_base.news
print("Start to collect articles from XKB.com.")

for x in range(1, 2):
    page_link = link + "list_270_" + str(x) + ".html"
    html = requests.get(page_link, headers = config.header)
    soup = BeautifulSoup(html.content)
    main_tag = soup.find('div', id='main_l_mcolumn')
    #get the article list from web page
    for blocks in main_tag.find_all('div', class_='al'):
        title = blocks.find('div', class_='al_title')
        article_id_raw.update(title.a['href'].encode('utf-8'))
        search_result = news_collection.find_one({"md5":article_id_raw.hexdigest()},{'_id':1})
        if not search_result:
            pub_time = blocks.find("div", class_= "al_pubdate").text#!/usr/bin/env python3
            pub_time.replace("\xa0",' ')
            article_id = news_collection.insert({"md5":article_id_raw.hexdigest()})
            articles[article_id]={}
            articles[article_id]['pub_time'] = pub_time
            articles[article_id]['title'] = title.text
            articles[article_id]['url'] = "http://www.xkb.com.au" + title.a['href']
            articles[article_id]['source'] = 'xkb';
            print('正在准备: ' + title.text)
        else:
            print(title.text + " 已经采集过了，无需再次采集！")
total_items = len(articles)
#get the detail information from inside pages.
for article_id, article in articles.items():
    counter += 1
    print('Start to get: %d/%d %s'%(counter,total_items,article['title']))
    time.sleep(random.randint(1, 3))
    article_html = requests.get(article['url'])
    article_soup = BeautifulSoup(article_html.content)
    article_main = article_soup.find('div', id='mid', class_='leftarea arc_body')
    articles[article_id]['content'] = article_main.text
    articles[article_id]['status'] = 0
    imgs = [x['src'] for x in article_main.findAll('img')]
    #test if the link is coming with a domain address
    if any(domain in s for s in imgs):
        articles[article_id]['imgs'] = imgs
    elif imgs:
        for key, img in enumerate(imgs):
            imgs[key] = 'http://' + domain + img
            articles[article_id]['imgs'] = imgs
for ids, keys in articles.items():
    result = news_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
    if result:
        print("入库成功: " + str(articles[ids]['title']))

print("We have got %d items in total" % counter)
config.data_base.logout()
config.data_client.close()

print('Now We are doing the injection')
news = requests.get('http://www.maifang.com.au/wp-content/themes/Focus/wordpress_injection/xkb.php?act=kslr')