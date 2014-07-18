__author__ = 'Han'

import pymongo
from pymongo import MongoClient

#Get ready for the database
data_client = MongoClient()
data_base = data_client.EZYProperty
#add authenticate for the MongoDB
#data_base.authenticate('EZYProperty', '8jshf7asd')
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"}
