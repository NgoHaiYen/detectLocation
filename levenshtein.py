from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.Fb_Raw

location = db.vn_location


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

    return previous_row[-1]


def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


class Group:
    gid = 0
    position = []

    def size(self):
        return len(self.position)

    def length(self):
        sum = 0
        for s in self.position:
            sum += len(s)
        return sum

    def averageLength(self):
        return self.length() / self.size()

    def distance(self, s):  # smaller is better
        distance = 0
        for value in self.position:
            distance += levenshtein(value, s)
            # should check the first character per word
        return distance / self.length()

    def addWord(self, word):
        self.position.append(word)

    def __str__(self):
        return str(self.gid) + ": " + str(self.position)

    def __init__(self, groupId):
        self.position = []
        self.gid = groupId


def findGroupById(group, groupId):
    for i in range(len(group)):
        if group[i].gid == groupId:
            return i
    return None


def getNumberOfElement(listGroup):
    sum = 0
    for group in listGroup:
        sum += group.size()
    return sum


import random


def match(listGroup):
    value = random.uniform(0.0, 1.0)
    n = getNumberOfElement(listGroup)
    total = 0
    for group in listGroup:
        total += group.size() / n
        if (total >= value):
            return group.gid
    return 0


def matchGroup(g, word, threshold):
    nearest = 100
    bestMatch = -1
    matches = []
    for i in range(len(g)):
        distance = g[i].distance(word)
        if distance < nearest:
            nearest = distance
            bestMatch = i
            matches = []
        elif distance == nearest:
            matches.append(g[i])

    if nearest < threshold:
        if len(matches) > 0:
            result = match(matches)
            g[findGroupById(g, result)].addWord(word)
        else:
            g[bestMatch].addWord(word)
    else:
        newGroup = Group(0)
        newGroup.addWord(word)
        g.append(newGroup)

    return g


data = location.find().limit(100000)
groupResult = []
threshold = 0.2
for d in data:
    groupResult = matchGroup(groupResult, d["location"], threshold)

for g in groupResult:
    print(g)
