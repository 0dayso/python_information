__author__ = 'yuerzx'

import csv
import pymongo
from pymongo import MongoClient
data_client = MongoClient()
data_base = data_client.Locations
#add authenticate for the MongoDB
data_base.authenticate('EZYProperty', '8jshf7asd')
super_c = data_base.supermarket

counter = 0
err_counter = 0
with open("/home/yuerzx/Desktop/woolworth_geo.csv", 'r', newline = '') as market_list:
    reader = csv.reader(market_list, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    next(reader)
    for row in reader:
        data = { "loc" :
                     { "type": "Point", "coordinates": [ float(row[8]), float(row[7]) ] },
                 "S_Type"   : row[0],
                 "S_Id"     : row[1],
                 "S_Name"   : row[2],
                 "Suburb"   : row[3],
                 "State"    : row[4],
                 "PCode"    : row[5],
                 "Phone"    : row[6],
                 "F_Address": row[9],
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