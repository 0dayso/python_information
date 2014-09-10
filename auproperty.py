#!/usr/bin/env python3

__author__ = 'yuerzx'

import requests
from bs4 import BeautifulSoup
import hashlib
import config
import time
import random
import re

articles = {}
domain = 'www.ausproperty.cn'
link = 'http://www.ausproperty.cn/instruction/strategy/'
counter = 0
#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()
#Get ready for the database
news_collection = config.data_base.news
print("Start to collect articles from AusProperty.cn .")
for x in range(1, 2):
    page_link = link + "list_117_" + str(x) + ".html"
    html = requests.get(page_link, headers = config.header)
    soup = BeautifulSoup(html.content)
    main_tag = soup.find('div', class_='listbox')
    #get the article list from web page
    for blocks in main_tag.find_all('li'):
        title = blocks.b.text
        full_url = domain + blocks.a['href']
        article_id_raw.update(full_url.encode('utf-8'))
        search_result = news_collection.find_one({"md5":article_id_raw.hexdigest()},{'_id':1})
        if not search_result:
            pub_time_pre = blocks.find("span", class_= "info")
            pub_time = re.search('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', pub_time_pre.text)
            article_id = news_collection.insert({"md5":article_id_raw.hexdigest()})
            articles[article_id]={}
            articles[article_id]['pub_time'] = pub_time.group(0)
            articles[article_id]['title'] = title
            articles[article_id]['url'] = 'http://' + full_url
            print('正在准备: ' + title)
        else:
            print(title + " 已经采集过了，无需再次采集！")
total_items = len(articles)

#get the detail information from inside pages.
for article_id, article in articles.items():
    counter += 1
    print('Start to get: %d/%d %s'%(counter,total_items,article['title']))
    time.sleep(random.randint(1, 3))
    article_html = requests.get(article['url'])
    article_soup = BeautifulSoup(article_html.content)
    article_main = article_soup.find('div', class_="content")
    articles[article_id]['content'] = article_main.text
    articles[article_id]['status'] = 0
    #mark out all the sourcing for our articles.
    articles[article_id]['source'] = 'auproperty'
    articles[article_id]['category'] = 'buyer-guide'
    imgs = [x['src'] for x in article_main.findAll('img')]
    #test if the link is coming with a domain address
    if any(domain in s for s in imgs):
        articles[article_id]['imgs'] = imgs
    elif any("http://" in s for s in imgs):
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
#news = requests.get('http://www.maifang.com.au/wp-content/themes/Focus/wordpress_injection/xkb.php?act=kslr')