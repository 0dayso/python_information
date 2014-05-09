__author__ = 'root'

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import pymongo
from pymongo import MongoClient


html = requests.get('http://xkb.com.au/html/caifu/dichantouzi/')

soup = BeautifulSoup(html.content)
main_tag = soup.find('div', id='main_l_mcolumn')
articles = {}
domain = 'www.xkb.com.au'
#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()

#Get ready for the database
news_collection = MongoClient().EZYProperty.news


#get the article list from webpage
for title in main_tag.find_all('div', class_='al_title'):
    article_id_raw.update(title.text.encode('utf-8'))
    article_id = news_collection.insert({"md5":article_id_raw.hexdigest()})
    articles[article_id]={}
    articles[article_id]['title'] = title.text
    articles[article_id]['url'] = "http://www.xkb.com.au" + title.a['href']
    print(title.text)
#get the detail information from inside pages.
for article_id, article in articles.items():
    article_html = requests.get(article['url'])
    article_soup = BeautifulSoup(article_html.content)
    article_main = article_soup.find('div', id='mid', class_='leftarea arc_body')
    articles[article_id]['content'] = article_main.text
    imgs = [x['src'] for x in article_main.findAll('img')]
    if(imgs and domain not in imgs):
        for key, img in enumerate(imgs):
            imgs[key] = 'http://' + domain + img
            articles[article_id]['imgs'] = imgs
    elif imgs:
        articles[article_id]['imgs'] = imgs

for ids, keys in articles.items():
    result = news_collection.update({'_id':ids},{"$set":keys}, upsert=False)
    if result:
        print(str(articles[ids]['title']) + " 入库成功 :)")
