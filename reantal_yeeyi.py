__author__ = 'yuerzx'
from bs4 import BeautifulSoup
import requests
import pre_process
import re
import time

#hide the system as a chrome
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
html = requests.get("http://www.yeeyi.com/bbs/forum.php?mod=viewthread&tid=1481166", headers=header)
index = BeautifulSoup(html.content,from_encoding='GBK')
#Get the publishing data
time_pub = pre_process.get_publish_time(index)

#Prepare all the documents content
page_content = index.find('td', class_='t_f')
pre_process.cleanup_marks(page_content)
item = pre_process.information_pickup(page_content)
item["publish_time"] = time_pub
print(item)
