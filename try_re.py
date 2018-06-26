import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.Fb_Raw
world_location = db.location
vietnam_location = db.vn_location
foreign_location = db.fo_location
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents2(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

def load_data_csv(filename):
    csvDataFile = open(filename)
    dataset = csv.reader(csvDataFile)
    dataset = list(dataset)
    csvDataFile.close()
    return dataset

def load_data_db(database):
    dictlist = []
    for value in database.find():
          if value["location"] == None:
                value["location"] = ""
          temp = [value["_id"],value["location"]]
          dictlist.append(temp)
    return dictlist
    
def clean(string):
    newItem = remove_accents2(string)
    newItem = newItem.lower()
    newItem = newItem.replace(" ", "")
    return newItem

def clean_facebook_data(database):
    fbdata = []
    
    dataset = load_data_db(database)
    for info in dataset:
       
        info[1] = clean(info[1])
        if info not in fbdata:
            fbdata.append(info)
    return fbdata

def clean_standard_info(filename):
    data = []
    city_list = []
    dataset = load_data_csv(filename)
    dataset = dataset[1:]
    for info in dataset:
        info[1] = clean(info[1])
        if info not in data:
            data.append(info)
            city_list.append(info[1])
    return data, city_list
 
 from fuzzywuzzy import process

def get_matches(query, choices, limit = 3):
    results = process.extract(query, choices, limit = limit)
    return results

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]/(len(s2)+len(s1)/2)

def domestic_filter(standard, facebook, threshold):
    domestic = {"_id" : "", "name" : "" }
    temp = []
    all = []
    std_data, city_list = clean_standard_info(standard)
    ori_data = load_data_db(facebook)
    fb_data = clean_facebook_data(facebook)
    for item in fb_data:
        i = 0
        curr_score = 10000000000
        most_simi = []
        print("------------------------")
        print(item)
        for stan in fb_data:
            
            distance = levenshtein(item[1], stan[1])
            if distance < threshold:
#                     curr_score = distance
                most_simi = ori_data[fb_data.index(stan)]
                print(most_simi)
                i = i + 1
                ori_data.remove(ori_data[fb_data.index(stan)])
                fb_data.remove(stan)
        print(i)    
