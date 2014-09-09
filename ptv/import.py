__author__ = 'Han'


import csv
import pymongo
from pymongo import MongoClient
data_client = MongoClient()
data_base = data_client.Locations
#add authenticate for the MongoDB
#data_base.authenticate('EZYProperty', '8jshf7asd')
super_c = data_base.Transport

counter = 0
err_counter = 0
name = "Bus"
with open( name+"_step2_fix.csv", 'r', newline = '') as market_list:
    reader = csv.reader(market_list, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    next(reader)
    for row in reader:
        data = {
                 "SName"    : row[0],
                 "Type"     : name,
                 "Suburb"   : row[1],
                 "Link"     : row[4],
                 "loc" :
                     { "type": "Point", "coordinates": [ float(row[2]), float(row[3]) ] },
                }
        results = super_c.insert(data)
        if results:
            counter += 1
            print("Done with %s"%row[0])
        else:
            err_counter += 1
            print("Error")
            print(results)


super_c.ensure_index([("loc", pymongo.GEOSPHERE)])
print("Total result is %d with %d errors"%(err_counter+counter, err_counter))
data_client.close()