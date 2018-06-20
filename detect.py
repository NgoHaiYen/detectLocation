# encoding=utf8-
# Standard Location
import csv
import re

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


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
    for i in range(len(dataset)):
        if (dataset[i][0], dataset[i][1]) not in commune:
            commune.append((dataset[i][0], dataset[i][1]))
        if (dataset[i][2], dataset[i][3]) not in district:
            district.append((dataset[i][2], dataset[i][3]))
        if (dataset[i][4], dataset[i][5]) not in city:
            city.append((dataset[i][4], dataset[i][5]))
        if (dataset[i][6], dataset[i][7]) not in country:
            country.append((dataset[i][6], dataset[i][7]))
    for info in dataset:
        info = [s for s in info if not s.isdigit()]
        for item in info:
            newItem = remove_accents2(item)
            newItem = newItem.lower()
            newItem = newItem.replace(" ", "")
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


# standard_data = clean_standard_info("tinh_huyen_xa.csv")
# fb_data = clean_facebook_data('test.csv')
# --------------------------------------------------------------------------------------------------------------------------

# Faceook Location
def clean_facebook_data(filename):
    fbdata = []
    csvDataFile = open(filename)
    dataset = csv.reader(csvDataFile)
    dataset = list(dataset)
    csvDataFile.close()
    for info in dataset:
        info[1] = remove_accents2(info[1])
        info[1] = info[1].lower()
        info[1] = info[1].replace(" ", "")
        info[1] = re.sub(r'[^A-z]*[^,]*', ' ', info[1])
        info = [info[0]] + [x.strip() for x in info[1].split(',')]
        if info not in fbdata:
            fbdata.append(info)
    return fbdata

def removeCharacter(s):
    regex = r'(?![A-z])(?![,])'
    line = re.sub(regex, "", s)
    return line

print(removeCharacter("auerhgaoirhgaoijgr awhegoiawjg12143413AAWGTQAHG,.....,,,,"))

def domestic_filter(standard, facebook):
    domestic = []
    _, _, _, _, std_data = clean_standard_info(standard)
    fb_data = clean_facebook_data(facebook)
    foreign = fb_data[1:]
    for user in fb_data:
        for item in user:
            if item in std_data:
                domestic.append(user)
                foreign.remove(user)
                break
    return domestic, foreign


# domestic, foreign = domestic_filter("tinh_huyen_xa.csv", "test.csv")