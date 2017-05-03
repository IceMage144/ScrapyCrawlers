import scrapy
import re
import requests
from Crawler.items import LinkItem
from Crawler.util import *

forbs = ["File:", "Template:", "Wikipedia:", "#", "Help:", "Category:", "(disambiguation)"]

class Wiki1Spider(scrapy.Spider):
    name = "Wiki1"

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
        self.startSite = None
        self.stack = None

    def start_requests(self):
        self.startSite = input(Color("Enter the starting site:\n", 33))
        self.finishSite = input(Color("Enter the finishing site:\n", 33))
        if not (isAnWikiSite(self.startSite) and isAnWikiSite(self.finishSite)):
            print(Color("One or more of the sites entered aren't from wikipedia!", 31))
            return
        self.finishSite = getName(self.finishSite)
        self.prev = self.PageNode(getName(self.startSite), None)
        self.linksDic[self.prev.link] = False
        yield getRequest(self.startSite, self.parse)

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
                self.stack = [colector]
                yield returnResult(self.stack, self.prev, self.startSite, self.parse_two)
            else:
                nextSite = f"https://en.wikipedia.org/wiki/{self.prev.link}"
                yield getRequest(nextSite, self.parse)
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
                self.stack = [colector]
                yield returnResult(self.stack, self.prev, self.start, self.parse_two)
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

    def parse_two(self, response):
        print(Color(f"Retrieving paragraph from {self.stack[0]}", 34))
        word = response.xpath(f"//div[@class='mw-content-ltr']/p//a[@href='/wiki/{self.stack[1]}'][1]/text()").extract()[0]
        par = response.xpath(f"//div[@class='mw-content-ltr']/p[a/@href='/wiki/{self.stack[1]}'][1]").extract()[0]
        par = re.sub("<.*?>|\{.*?\}|\[.*?\]", "", par)
        match = re.search(f"\\b{word}\\b", par)
        par = par[:match.start()] + Color(word, 36) + par[match.end():]
        print(par)
        self.stack.remove(self.stack[0])
        if len(self.stack) <= 1:
            yield None
        yield scrapy.Request(url=f"https://en.wikipedia.org/wiki/{self.stack[0]}", callback=self.parse_two)
