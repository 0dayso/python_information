__author__ = 'Han'

import csv
import pymongo
from pymongo import MongoClient
data_client = MongoClient()
data_base = data_client.Locations
#add authenticate for the MongoDB
data_base.authenticate('EZYProperty', '8jshf7asd')
super_c = data_base.rental_media_reiv

counter = 0
err_counter = 0
with open("rental.csv", 'r', newline = '') as market_list:
    reader = csv.reader(market_list, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    next(reader)
    for row in reader:
        data = {
                 "Suburb"   : row[0],
                 "Date"     : "201403",
                 "Bed_Room" : row[1],
                 "Type"     : row[2],
                 "PWD"      : row[3]
                 }
        results = super_c.insert(data)
        if results:
            counter += 1
            print("Done with %s"%row[2])
        else:
            err_counter += 1
            print("Error")
            print(results)
print("Total result is %d with %d errors"%(err_counter+counter, err_counter))