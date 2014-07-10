__author__ = 'yuerzx'

#details files can be download from
# https://www.wowlink.com.au/wps/portal/!ut/p/c0/04_SB8K8xLLM9MSSzPy8xBz9CP0os3izQB8jJydDRwMDA2djA6Mg_zDHsNBgYwMLc_2CbEdFAEZfwvU!/?WCM_PORTLET=PC_7_6QL2BB1A00C1802R41RJCD1082_WCM&WCM_GLOBAL_CONTEXT=/cmgt/wcm/connect/content+library+-+wowlink/WOWLink/Contacts/StoreContacts/

#aim of this program is that read data from store list csv file and then use google maps to get geocode from google

import csv
import requests
import google_maps_api
import time

with open('/home/yuerzx/Desktop/woolworth.csv', 'r', newline='') as store_list, open('woolworth_geo.csv', "w", newline='') as store_list_geo:
    reader = csv.reader(store_list, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    writer = csv.writer(store_list_geo, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    header = ['S_Type','S_Id', 'S_Name', 'Suburb', 'State', 'PCode', 'Phone', 'lat', 'lng', 'Full_Address', 'link']
    #write header for new file
    writer.writerow(header)
    to_counter, err_counter = 0, 0
    next(reader)
    for row in reader:
        store_address = ''
        short_address = ''
        S_Id = ''
        to_counter += 1
        err_code = 0
        for x in range(3, 6):
            short_address += row[x] + ' '
        store_address = 'Woolworth ' + short_address + ' Australia '
        store_address += row[6]
        print('I am processing '+ row[2])
        #send data to google
        for x in range(0, 2):
            break_point = False
            #try twice for every data
            location = google_maps_api.google_decode(store_address)
            if location['status'] != 'OK':
                print('Something wrong with google maps and we are going to stop now!!')
                print(location)
                err_counter += 1
                err_code = 1
            else:
                break_point         = True
                lat                 = location['results'][0]['geometry']['location']['lat']
                lng                 = location['results'][0]['geometry']['location']['lng']
                location_components = location['results'][0]['address_components']
            if break_point == True:
                break
        if err_code == 1:
            print('Err with Google Maps')
            writer.writerow(['Woolworth', str(row[0]), str(row[2]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), 'Error', 'Error', str(short_address), ''])
        else:
            writer.writerow(['Woolworth', str(row[0]), str(row[2]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(lat), str(lng), str(short_address), ''])
            print('Finish, success :)')
        #in case over the limited of google maps, we use timer to limited it
        time.sleep(0.5)
    print("Total items are %d and %d errors. " % (to_counter, err_counter))