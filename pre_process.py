__author__ = 'yuerzx'

import re
import time
import hashlib
from pymongo import MongoClient

#Get ready for the database
rental_client = MongoClient()
rental_collection = rental_client.EZYProperty.rental
domain = "yeeyi.com/bbs/"

def yeeyi_title_process(item):
    """
    :rtype : string
    """
    if "房屋" in item:
        if "来源" in item:
            return "Property Source"
        elif "租金" in item:
            return "Property Rent"
        elif "户型" in item:
            return "Property Rooms"
    elif "详细" in item:
        if "地址" in item:
            return "Address"
        elif "介绍" in item:
            return "Details"
    elif "联" in item:
        if "人" in item:
            return "Contacts"
        elif "电话" in item:
            return "Phone"
    elif "入住" and "时间" in item:
        return "Available:"
    elif "出租" and "方式" in item:
        return "Rental Type"
    elif "性别" and "要求" in item:
        return "Roommate Prefer"
    elif "QQ" and "号码" in item:
        return "QQ"
    else:
        return "Unknown!" + item

yeeyi_dict={
    '男女不限':'Either',
    '限女生':'Female',
    '限男生':'Male',
    '整租':'Takeover',
    '转租':'Contract Transfer',
    '单间':'Room',
    'Share':'Room',
    '客厅':'living Room',
    '其它':'Other',
    '个人':'Personal'
}

#TODO Start to handle the time and clean all the time up.
def yeeyi_content_process(content):
    # Actually this is a dictionary function to convert chinese to english
    not_find = "Unknown! " + str(content)
    return yeeyi_dict.get(content,not_find)

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
            item_title = str(yeeyi_title_process(p.span.text))
            p.span.extract()
            item_content = re.sub('\\xa0', '', p.text)
            if item_title == "Property Rooms":
                item_content = get_rooms(item_content)
            elif item_title == "Phone": #vaild phone number
                phone_vaild = re.search("\d{9,11}", item_content)
                if phone_vaild:
                    item_content = phone_vaild.group(0)
                else:
                    item_content = "Unknown!" + item_content
            #skip content
            elif item_title == "Details":
                item_content = item_content
            elif item_title == "Address":
                item_content = item_content
            else:
                item_content = yeeyi_content_process(item_content)
            item[item_title] = item_content
    #find out all the images
    imgs =[img['src'] for img in page_content.find_all('img')]
    item['org_imgs']=imgs
    if any(domain in s for s in imgs):
        item['org_imgs'] = imgs
    elif imgs:
        for key, img in enumerate(imgs):
            imgs[key] = 'http://' + domain + img
            item['org_imgs'] = imgs
    return item


def get_rooms(item):
    #aim to get all the rooms such as bed room, living room, car park and so on
    list_rooms = list(item)
    #bedroom
    position = [i for i, x in enumerate(list_rooms) if x == "室"]
    if position:
        bedroom = int(list_rooms[(position[0]-1)])
    else:
        bedroom = 0
    position = [i for i, x in enumerate(list_rooms) if x == "厅"]
    if position:
        living_room = int(list_rooms[(position[0]-1)])
    else:
        living_room = 0
    position = [i for i, x in enumerate(list_rooms) if x == "卫"]
    if position:
        bath_room = int(list_rooms[(position[0]-1)])
    else:
        bath_room = 0
    position = [i for i, x in enumerate(list_rooms) if x == "阳"]
    if position:
        balcony = int(list_rooms[(position[0]-1)])
    else:
        balcony = 0
    return {"bedroom":bedroom,"living Room": living_room, "Bath Room": bath_room, "Balcony":balcony}

def front_page_links(home_index):
    links= {}
    article_id_raw = hashlib.md5()
    home_links = home_index.find("ul", class_="cgl cl")
    for ls in home_links.find_all("a"):
        article_id_raw.update(ls['href'].encode("utf-8"))
        links[article_id_raw.hexdigest()] = ls['href']
        search_result = rental_collection.find_one({"md5":article_id_raw.hexdigest()},{'_id':1})
        if search_result:
            del links[article_id_raw.hexdigest()]
    return links

def get_page_title(index):
    #get the title for current page
    title = (index.find('a', id="thread_subject")).text
    return str(title)

def get_publish_time(index):
    #Get the publishing data
    time_stamp_pre = index.find('div', class_="pti")
    time_stamp_pre = re.search("\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}",time_stamp_pre.em.text)
    if time_stamp_pre:
        time_stamp = time.strptime(time_stamp_pre.group(0),"%Y-%m-%d %H:%M")
        time_pub = time.strftime("%d-%m-%Y %H:%M", time_stamp)
    else:
        time_pub = "Unknown!" + (index.find('div', class_="pti")).em.text
    return time_pub