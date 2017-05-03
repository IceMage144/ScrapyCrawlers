import json
import re
from pathlib import Path

def loadDatabase(name):
    fileName = "conv_%s_articles.json" % name[:-1]
    path = Path(fileName)
    dic = {}
    if path.is_file():
        print(Color("Loading database...", 33))
        dic = json.load(open(fileName))
        print(Color("Finish loading", 32))
        return dic
    else:
        print(Color("Database not found", 31))
    return dic

def convert(name):
    lines = []
    dic = {}
    original = f'{name}_articles.jl'
    newName = "conv_%s_articles.json" % name[:-1]
    path = Path(newName)
    if path.is_file():
        print(Color("Loading database...", 33))
        dic = json.load(open(newName))
        print(Color("Finish loading", 32))
    with open(original) as f:
        k = f.readlines()
    print(Color("Converting new itens...", 33))
    dic["!!Number_Of_Entries!!"] = 0
    for line in k:
        entry = json.loads(line)
        dic[entry["name"]] = entry["links"]
    dic["!!Number_Of_Entries!!"] = len(dic)-1
    print(Color("Finish converting", 32))
    with open(newName, "w+") as f:
        f.write(json.dumps(dic, sort_keys=True, indent=1))
        print(Color("Saved database", 32))

def Color(string, num):
    return (f"\033[1;{num}m{string}\033[0m")

def isAnWikiSite(string):
    return (re.search("https://en.wikipedia.org/wiki/", string) != None)

def returnResult(stack, prev, site, callback):
    print(Color("=============== Result ===============", 36))
    ptr = prev
    while (ptr != None):
        stack.insert(0, ptr.link)
        ptr = ptr.prev
    for link in stack:
        print(Color(link, 36))
    return getRequest(site, callback)
    print(Color("======================================", 36))

def getRequest(site, callback):
    try:
        req = requests.get(site)
        if req.status_code == 200:
            print(Color(f"Searching at {site}", 32))
            return scrapy.Request(site, callback=callback, dont_filter=True)
        else:
            print(Color(f"Can't connect to {site}", 31))
    except requests.exceptions.ConnectionError:
        print(Color(f"Can't connect to {site}", 31))

def getName(url):
    return url.split("/")[-1]

def haveForbs(string):
    res = False
    for forb in forbs:
        if re.search(forb, string) != None:
            res = True
    return res
