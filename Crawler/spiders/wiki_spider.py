import scrapy
import re
import requests
from Crawler.items import LinkItem
from Crawler.util import *

forbs = ["File:", "Template:", "Wikipedia:", "#", "Help:", "Category:", "(disambiguation)"]

class WikiSpider(scrapy.Spider):
    name = "Wiki"

    class PageNode:
        def __init__(self, link, prev):
            self.link = link
            self.prev = prev

    def __init__(self):
        self.dataDic = loadDatabase(self.name)
        self.linksDic = {}
        self.queue = []
        self.prev = None
        self.finishSite = None

    def start_requests(self):
        startSite = input(Color("Enter the starting site:\n", 33))
        self.finishSite = input(Color("Enter the finishing site:\n", 33))
        if not (isAnWikiSite(startSite) and isAnWikiSite(self.finishSite)):
            print(Color("One or more of the sites entered aren't from wikipedia!", 31))
        self.finishSite = getName(self.finishSite)
        self.prev = self.PageNode(getName(startSite), None)
        self.linksDic[self.prev.link] = False
        try:
            req = requests.get(startSite)
            if req.status_code == 200:
                print(Color(f"Searching at {startSite}", 32))
                yield scrapy.Request(url=startSite, callback=self.parse)
            else:
                print(Color(f"Can't connect to {startSite}", 31))
        except requests.exceptions.ConnectionError:
            print(Color(f"Can't connect to {startSite}", 31))

    def parse(self, response):
        found = False
        colector = None
        dbList = self.dataDic.get(getName(response.url))
        if dbList != None:
            counter = 0
            while (dbList != None and not found):
                for link in dbList:
                    if self.linksDic.get(link) == None:
                        if link != self.finishSite:
                            self.queue.insert(0, self.PageNode(link, self.prev))
                            self.linksDic[link] = False
                        else:
                            found = True
                            colector = link
                if not found:
                    tmp = self.queue.pop()
                    if tmp.prev != self.prev.prev:
                        print(Color(f"Searching at {tmp.prev.link} pages", 33))
                    self.prev = tmp
                    dbList = self.dataDic.get(getName(self.prev.link))
                counter += 1
            print(Color(f"Got {counter} entries from database", 34))
            if found:
                print(Color("=============== Result ===============", 36))
                stack = [colector]
                ptr = self.prev
                while (ptr != None):
                    stack.insert(0, ptr.link)
                    ptr = ptr.prev
                for link in stack:
                    print(Color(link, 36))
                print(Color("======================================", 36))
            else:
                try:
                    nextSite = f"https://en.wikipedia.org/wiki/{self.prev.link}"
                    req = requests.get(nextSite)
                    if req.status_code == 200:
                        print(Color(f"Searching at {nextSite}", 32))
                        yield scrapy.Request(url=nextSite, callback=self.parse)
                    else:
                        print(Color(f"Can't connect to {nextSite}", 31))
                except requests.exceptions.ConnectionError:
                    print(Color(f"Can't connect to {nextSite}", 31))
        else:
            listLinks = {}
            links = response.xpath('//div[@class="mw-content-ltr"]/p//a/@href').extract() #extracting links
            for link in links:
                if link[:5] == "/wiki" and (not haveForbs(link)):
                    link = link[6:]
                    if self.linksDic.get(link) == None:
                        if link != self.finishSite:
                            self.queue.insert(0, self.PageNode(link, self.prev))
                            self.linksDic[link] = False
                        else:
                            found = True
                            colector = link
                    listLinks[link] = False
            yield LinkItem(name=getName(response.url), links=list(listLinks.keys()))
            if found:
                stack = [colector]
                ptr = self.prev
                while (ptr != None):
                    stack.insert(0, ptr.link)
                    ptr = ptr.prev
                for link in stack:
                    print(Color(link, 36))
            else:
                try:
                    tmp = self.queue.pop()
                    if tmp.prev != self.prev.prev:
                        print(Color(f"Searching at {tmp.prev.link} pages", 33))
                    self.prev = tmp
                    nextSite = f"https://en.wikipedia.org/wiki/{self.prev.link}"
                    req = requests.get(nextSite)
                    if req.status_code == 200:
                        print(Color(f"Searching at {nextSite}", 32))
                        yield scrapy.Request(url=nextSite, callback=self.parse)
                    else:
                        print(Color(f"Can't connect to {nextSite}", 31))
                except requests.exceptions.ConnectionError:
                    print(Color(f"Can't connect to {nextSite}", 31))

def isAnWikiSite(string):
    return (re.search("https://en.wikipedia.org/wiki/", string) != None)

def getName(url):
    return url.split("/")[-1]

def haveForbs(string):
    res = False
    for forb in forbs:
        if re.search(forb, string) != None:
            res = True
    return res


#def justify(text):
#    words = list(filter(None, text.split(" ")))
#    lines = []
#    for i in range(0, len(words), 15):
#        arr = []
#        for j in range(15):
#            if (i+j < len(words)):
#                arr.append(words[i+j])
#        lines.append(" ".join(arr))
#    return "\n".join(lines)
