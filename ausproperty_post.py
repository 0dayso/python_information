#!/usr/bin/env python3

__author__ = 'yuerzx'

import requests
from bs4 import BeautifulSoup
import hashlib
import config
import time
import random
import re
import json

articles = {}
domain = 'www.ausproperty.cn'
link = 'http://www.ausproperty.cn/instruction/strategy/'
inject_port = 'http://www.maifang.com.au/wp-content/themes/Focus/wordpress_injection/data-inject.php'
counter = 0
error = 0
inner_counter = 0
#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()
#Get ready for the database
print("Start to collect articles from AusProperty.cn .")
for x in range(1, 5):
    page_link = link + "list_117_" + str(x) + ".html"
    html = requests.get(page_link, headers = config.header)
    soup = BeautifulSoup(html.content)
    main_tag = soup.find('div', class_='listbox')
    #get the article list from web page
    for blocks in main_tag.find_all('li'):
        title = blocks.find('a', class_='title').text
        if config.check_exist(title):
            full_url = domain + blocks.a['href']
            article_id_raw.update(full_url.encode('utf-8'))
            pub_time_pre = blocks.find("span", class_= "info")
            pub_time = re.search('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', pub_time_pre.text)
            article_id = article_id_raw.hexdigest()
            articles[article_id]={}
            articles[article_id]['pub_time'] = pub_time.group(0)
            articles[article_id]['title'] = title
            articles[article_id]['url'] = 'http://' + full_url
            articles[article_id]['act'] = 'kslr'
            print('正在准备: ' + title)
        else:
            print('已经采集: ' + title)
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
        block_set[article_id]['act'] = 'kslr'
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
    if inner_counter>= 5:
        for ids, keys in block_set.items():
            try:
                result = requests.post(inject_port, data = json.dumps(keys))
                status_code = json.loads(result.text)
                if status_code['Status'] == 'Success':
                    print("Successfully inject %s" % keys['title'])
                else:
                    print(status_code)
                    print("Error")
            except:
                pass
        block_set={}
        inner_counter = 0
        print("Here here and here!!!")
for ids, keys in block_set.items():
    try:
        result = requests.post(inject_port, data = json.dumps(keys))
        status_code = json.loads(result.text)
        if status_code['Status'] == 'Success':
            print("Successfully inject %s" % keys['title'])
        else:
            print(status_code)
            print("Error")
    except:
        pass


