__author__ = 'Han'

import pymongo
from pymongo import MongoClient
import json
import requests

#Get ready for the database
data_client = MongoClient()
data_base = data_client.EZYProperty
#add authenticate for the MongoDB
#data_base.authenticate('EZYProperty', '8jshf7asd')
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}

def check_exist(title):
    try:
        keys={"title": title, "pass":"human" }
        result = requests.post('http://127.0.0.1/maifang/wp-content/themes/Focus/wordpress_injection/check.php', data = json.dumps(keys))
        status_code = json.loads(result.text)
        if status_code['Status'] == 'OK':
            return True
        else:
            return False
    except:
        return False