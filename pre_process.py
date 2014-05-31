__author__ = 'yuerzx'

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
    else:
        return "Unknown Item!" + item

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
    '个人':'Personal',

}

#TODO Start to handle the time and clean all the time up.
def yeeyi_content_process(content):
    # Actually this is a dictionary function to convert chinese to english
    not_find = "Unknow!" + content
    return yeeyi_dict.get(content,not_find)
