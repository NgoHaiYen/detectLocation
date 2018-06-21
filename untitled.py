# encoding=utf8-
#Standard Location
import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.Fb_Raw

location = db.vn_location

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

def clean(string):
    newItem = remove_accents2(string)
    newItem = newItem.lower()
    newItem = newItem.replace(" ", "")
    return newItem

def clean_standard_info(filename):
    data = []
    csvDataFile = open(filename)
    dataset = csv.reader(csvDataFile)
    dataset = list(dataset)
    csvDataFile.close()
    dataset = dataset[1:]
    commune = []
    district = []
    city = []
    country = []
    for i in range (len(dataset)):
        if dataset[i][1] not in commune:
            commune.append(dataset[i][0])
            commune.append(clean(dataset[i][1]))
        if dataset[i][3] not in district:
            district.append(dataset[i][2])
            district.append(clean(dataset[i][3]))
        if dataset[i][5] not in city:
            city.append(dataset[i][4])
            city.append(clean(dataset[i][5]))
        if dataset[i][7] not in country:
            country.append(dataset[i][6])
            country.append(clean(dataset[i][7]))
    for info in dataset:
        info = [s for s in info if not s.isdigit()]
        for item in info:
            newItem = clean(item)
            if newItem not in data:
                data.append(newItem)
    return commune, district, city, country, data
 
def remove_accents2(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s
 
standard_data = clean_standard_info("tinh_huyen_xa.csv")
#fb_data = clean_facebook_data('test.csv')
#--------------------------------------------------------------------------------------------------------------------------

#Faceook Location  
def clean_facebook_data(filename):
    fbdata = []
    csvDataFile = open(filename)
    dataset = csv.reader(csvDataFile)
    dataset = list(dataset)
    csvDataFile.close()
    for info in dataset:
       
        info[1] = clean(info[1])
        info = [info[0]] + [x.strip() for x in info[1].split(',')]
        if info not in fbdata:
            fbdata.append(info)
    return fbdata

def domestic_filter(standard, facebook):
    domestic = []
    _ , _ , _, _, std_data = clean_standard_info(standard)
    fb_data = clean_facebook_data(facebook)
    foreign = fb_data[1:]
    for user in fb_data:
        for item in user:
            if item in std_data:
                domestic.append(user)
                foreign.remove(user)
                break
    return domestic, foreign
                
domestic, foreign = domestic_filter("tinh_huyen_xa.csv", "test.csv" )
location.insert_many(domestic)

first = domestic[0]

'''def create_tag(user, std_data):
    commune, district, city, country = std_data
    domestic_tag = {commune: "", district: "", city: "", country: "vn84"}
    for item in reversed(user):
        if item in country:
            pass
        elif item in city:
            if domestic_tag["city"] == "":
                domestic_tag["city"] = city[city.index(item) - 1]
        elif item in district:
            if domestic_tag["city"] == "":
                domestic_tag["city"] = city[district.index(item) - 1]
            domestic_tag["district"] = district[district.index(item) - 1]
        elif item in commune:
            if domestic_tag["district"] == "":
                domestic_tag["district"] = city[commune.index(item) - 1]
            if domestic_tag["city"] == "":
                domestic_tag["city"] = city[district.index(item) - 1]'''
        

