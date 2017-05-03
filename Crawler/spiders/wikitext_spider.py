import scrapy
import re
import requests
from Crawler.util import *
from Crawler.items import TextItem

class TextSpider(scrapy.Spider):
    name = "Text1"

    def start_requests(self):
        site = input(Color("Enter the site:\n", 33))
        if not (isAnWikiSite(site)):
            print(Color("The site entered isn't from wikipedia!", 31))
            return
        try:
            req = requests.get(site)
            if req.status_code == 200:
                print(Color(f"Searching at {site}", 32))
                yield scrapy.Request(url=site, callback=self.parse)
            else:
                print(Color(f"Can't connect to {site}", 31))
        except requests.exceptions.ConnectionError:
            print(Color(f"Can't connect to {site}", 31))

    def parse(self, response):
        page = response.css("div.mw-content-ltr p").extract()
        for i in range(len(page)):
            page[i] = re.sub("<.*?>|\{.*?\}|\[.*?\]", "", page[i])
        page = list(filter(None, page))
        text = "\n".join(page)
        print(text)
        yield TextItem(link=response.url, text=text)

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
