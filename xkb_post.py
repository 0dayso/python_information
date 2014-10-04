__author__ = 'Han'

import requests
from bs4 import BeautifulSoup
import hashlib
import time
import random
import json
import config


articles = {}
domain = 'www.xkb.com.au'
link = 'http://xkb.com.au/html/caifu/dichantouzi/'
inject_url = 'http://www.maifang.com.au/wp-content/themes/Focus/wordpress_injection/data-inject.php'
counter = 0
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}

#Use the hash value of article title as a unique id
article_id_raw = hashlib.md5()
#Get ready for the database
print("Start to collect articles from XKB.com.")

for x in range(1, 5):
    page_link = link + "list_270_" + str(x) + ".html"
    html = requests.get(page_link, headers = header)
    soup = BeautifulSoup(html.content)
    main_tag = soup.find('div', id='main_l_mcolumn')
    #get the article list from web page
    for blocks in main_tag.find_all('div', class_='al'):
        title = blocks.find('div', class_='al_title')
        title_txt = title.text
        if config.check_exist(title_txt):
            pub_time = blocks.find("div", class_= "al_pubdate").text
            pub_time.replace("\xa0",' ')
            article_id_raw.update(title.a['href'].encode('utf-8'))
            article_id = article_id_raw.hexdigest()
            articles[article_id]={}
            articles[article_id]['pub_time'] = pub_time
            articles[article_id]['title'] = title.text
            articles[article_id]['url'] = "http://www.xkb.com.au" + title.a['href']
            articles[article_id]['source'] = 'xkb'
            print('正在准备: ' + title_txt)
        else:
            print('已经采集: ' + title_txt)

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
    articles[article_id]['act'] = 'kslr'
    imgs = [x['src'] for x in article_main.findAll('img')]
    #test if the link is coming with a domain address
    if any(domain in s for s in imgs):
        articles[article_id]['imgs'] = imgs
    elif imgs:
        for key, img in enumerate(imgs):
            imgs[key] = 'http://' + domain + img
            articles[article_id]['imgs'] = imgs
for ids, keys in articles.items():
    try:
        result = requests.post(inject_url, data = json.dumps(keys))
        status_code = json.loads(result.text)
        if status_code['Status'] == 'Success':
            print("Successfully inject %s" % keys['title'])
        else:
            print(status_code)
            print("Error")
    except:
        print("Error")

print("We have got %d items in total" % counter)
