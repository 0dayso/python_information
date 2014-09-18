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
error = 0
inner_counter = 0
#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()
#Get ready for the database
news_collection = config.data_base.news
print("Start to collect articles from AusProperty.cn .")
for x in range(1, 10):
    page_link = link + "list_117_" + str(x) + ".html"
    html = requests.get(page_link, headers = config.header)
    soup = BeautifulSoup(html.content)
    main_tag = soup.find('div', class_='listbox')
    #get the article list from web page
    for blocks in main_tag.find_all('li'):
        title = blocks.find('a', class_='title').text
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
block_set = {}
#get the detail information from inside pages.
for article_id, article in articles.items():
    counter += 1
    inner_counter += 1
    block_set[article_id]={}
    block_set[article_id]['url'] = articles[article_id]['url']
    block_set[article_id]['title'] = articles[article_id]['title']
    block_set[article_id]['pub_time'] = articles[article_id]['pub_time']
    print('Start to get: %d/%d %s'%(counter,total_items,article['title']))
    time.sleep(random.randint(1, 10))
    try:
        article_html = requests.get(article['url'])
        article_soup = BeautifulSoup(article_html.content)
        article_main = article_soup.find('div', class_="content")
        block_set[article_id]['content'] = article_main.text
        block_set[article_id]['status'] = 0
        #mark out all the sourcing for our articles.
        block_set[article_id]['source'] = 'ausproperty'
        block_set[article_id]['category'] = 'buyer-guide'
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
    except:
        block_set[article_id]['status'] = 'error'
        error += 1
    if inner_counter>= 10:
        for ids, keys in block_set.items():
            result = news_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
            if result:
                print("入库成功: " + str(articles[ids]['title']))
        block_set={}
for ids, keys in block_set.items():
    result = news_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
    if result:
        print("入库成功: " + str(articles[ids]['title']))

print("We have got %d items in total with %d errors" % (counter,error))
#error fixing module the best part of the program

if error >= 1:
    print("Now we are fixing up the errors!")
    error_before =0
    article_fix = {}
    search_result = news_collection.find({'status':"error"},{'_id':1,'url':1})
    for article in search_result:
        try:
            article_html = requests.get(article['url'])
            article_soup = BeautifulSoup(article_html.content)
            article_main = article_soup.find('div', class_="content")
            article_fix['id'] = article['_id']
            article_fix['id']['content'] = article_main.text
            article_fix['id']['status'] = 0
            #mark out all the sourcing for our articles.
            article_fix['id']['source'] = 'ausproperty'
            article_fix['id']['category'] = 'buyer-guide'
            imgs = [x['src'] for x in article_main.findAll('img')]
            #test if the link is coming with a domain address
            if any(domain in s for s in imgs):
                article_fix['id']['imgs'] = imgs
            elif any("http://" in s for s in imgs):
                article_fix['id']['imgs'] = imgs
            elif imgs:
                for key, img in enumerate(imgs):
                    imgs[key] = 'http://' + domain + img
                    article_fix['id']['imgs'] = imgs
        except:
            error_before += 1
    for ids, keys in article_fix.items():
        result = news_collection.update({'_id': ids}, {"$set":keys}, upsert=False)
        if result:
            print("入库成功: " + str(articles[ids]['title']))
    print('We got %d error remain' % error_before)

config.data_base.logout()
config.data_client.close()

print('Now We are doing the injection')
#news = requests.get('http://www.maifang.com.au/wp-content/themes/Focus/wordpress_injection/ausproperty.php?act=kslr')