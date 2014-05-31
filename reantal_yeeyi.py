__author__ = 'yuerzx'
from bs4 import BeautifulSoup
import re
import requests
import pre_process

def cleanup_marks(page_content):
    #best way to clean up all the hidden information.
    span_count = 1
    font_count = 1
    for span in page_content.find_all('span', style='display:none'):
        span.decompose()
        span_count += 1
    for font in page_content.find_all('font', style = "font-size:10px;color:#FFF"):
        font.decompose()
        font_count += 1
    print("Finish all the cleaning up, I have find " + str(span_count) + " hidden span and " + str(font_count) + " hidden font")

def information_pickup(page_content):
    #this function is aiming at sort up all the information.
    item={}
    #clean up all the text
    for p in page_content.find_all('p'):
        if p.span:
            item_title = str(pre_process.yeeyi_title_process(p.span.text))
            p.span.extract()
            item_content = re.sub('\\xa0', '', p.text)
            if item_title != "Details":
                item_content = pre_process.yeeyi_content_process(item_content)
            item[item_title] = item_content
    #find out all the images
    imgs =[img['src'] for img in page_content.find_all('img')]
    item['imgs']=imgs
    if any(domain in s for s in imgs):
        item['imgs'] = imgs
    elif imgs:
        for key, img in enumerate(imgs):
            imgs[key] = 'http://' + domain + img
            item['imgs'] = imgs
    print(item)

#hide the system as a chrome
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
html = requests.get("http://www.yeeyi.com/bbs/forum.php?mod=viewthread&tid=1481166", headers=header)
index = BeautifulSoup(html.content,from_encoding='GBK')

domain = "yeeyi.com/bbs/"


page_content = index.find('td', class_='t_f')
cleanup_marks(page_content)
information_pickup(page_content)
