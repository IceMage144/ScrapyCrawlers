import scrapy
import re
from Crawler.util import *
from Crawler.items import WordItem

partOfSpeech = {"v"           : "Verb",
                "adj"         : "Adjective",
                "n"           : "Noun",
                "prep"        : "Preposition",
                "int"         : "Interjection",
                "adv"         : "Adverb",
                "symbol"      : "Symbol",
                "proper"      : "Proper_noun",
                "abbr"        : "Abbreviation",
                "infix"       : "Infix",
                "suffix"      : "Suffix",
                "prefix"      : "Prefix",
                "init"        : "Initialism",
                "acronym"     : "Acronym",
                "contraction" : "Contraction",
                "phrase"      : "Phrase",
                "proverb"     : "Proverb",
                "num"         : "Numeral",
                "part"        : "Participle",
                "article"     : "Article",
                "pronoun"     : "Pronoun",
                "conj"        : "Conjunction",
                "determiner"  : "Determiner",
                "prep-phrase" : "Prepositional_phrase",
                "circumfix"   : "Circumfix",
                "affix"       : "Interfix",
                "letter"      : "Letter",
                "particle"    : "Particle"}

verbForms = ["third-person singular simple present", "present participle",
             "simple past", "past participle"]

adjForms = ["comparative", "superlative"]

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class DictSpider(scrapy.Spider):
    name = "Dict1"

    def start_requests(self):
        site = input(Color("Enter the site:\n", 33))
        if not (isAnWiktSite(site)):
            print(Color("The site entered isn't from wiktionary!", 31))
            return
        yield getRequest(site, self.parse2)


    def parse(self, response):
        page = response.xpath("//div[@class='mw-content-ltr']/*")
        extrPage = page.extract()
        #strong = response.xpath("//p[strong/@class='Latn headword']").extract()
        headers = []
        rang = [-1, -1]
        forms = []
        genDict = {}
        # find english defined nodes
        for i in range(len(extrPage)):
            if extrPage[i][:4] == "<h2>":
                if "English" in extrPage[i]:
                    rang[0] = i+1
                elif rang[0] != -1 and rang[1] == -1:
                    rang[1] = i
                    break
        page = page[rang[0]:rang[1]]
        # find parts of speech

        for node in page:
            try:
                mem = node.xpath("span/@id").extract()[0]
            except IndexError:
                continue
            for pos in partOfSpeech.values():
                if (pos == mem) and (pos not in headers):
                    headers.append(pos)
        #    if "Latn headword" in node:
        #        forms.append(re.sub("<.*?>|\{.*?\}|\[.*?\]", "", node))
        headers = [s for s in headers if s in partOfSpeech.values()]
        '''if len(headers) != len(forms):
            print(Color("len(headers) = %d != len(forms) = %d".format(len(headers), len(forms)), 31)))
            print("headers =>", headers)
            print("forms =>", forms)
            return
        for pos, form in zip(headers, forms):
            v = form.split("(")
            if len(v) != 2:
                continue
            if pos == "Verb":
                if "irregular" in form:
                    print(Color(f"{form} is an irregular verb", 31))
                    continue
                genDict["Verb"] = verbParse(form.split("(")[1][:-1].replace(",", ""))
            elif pos == "Noun":
                genDict["Noun"] = nounParse(form.split("(")[1][:-1].replace(",", ""))
            elif pos == "Adjective":
                genDict["Adjective"] = adjParse(form.split("(")[1][:-1].replace(",", ""))'''
        word = response.url.replace("https://en.wiktionary.org/wiki/", "").replace("_", " ")
        print(Color(f"Found: {word} : {headers}", 32))
        yield WordItem(word=word, pos=headers)

    def parse2(self, response):
        li = response.xpath("//div[@class='index']//li")
        for node in li:
            word = node.xpath("a/text()").extract()[0]
            try:
                abbr = node.xpath("i/text()").extract()[0].split(" ")
            except IndexError:
                print(Color("Can't find POS:\n" + node.extract(), 31))
                if "page does not exist" not in node.xpath("a/@title").extract()[0]:
                    print("Trying to find POS in the original page")
                    site = "https://en.wiktionary.org" + node.xpath("a/@href").extract()[0]
                    yield getRequest(site, self.parse)
                continue
            pos = []
            for i in abbr:
                if (partOfSpeech.get(i) == None):
                    print(Color("Can't identify POS:\n" + node.extract(), 36))
                    continue
                pos.append(partOfSpeech[i])
            yield WordItem(word=word, pos=pos)

def verbParse(s):
    stk = []
    res = {}
    for c, i in zip(verbForms, range(4)):
        s = s.replace(c, str(i))
    v = s.replace("and ", "").split(" ")
    mark = True
    for i in v:
        if i in numbers:
            stk.append(i)
            mark = False
        else:
            if mark == True:
                continue
            for el in stk:
                res[verbForms[int(el)]] = i
            stk = []
            mark = True
    return res

def nounParse(s):
    res = {}
    v = s.split(" ")
    p = 0
    for i in range(len(v)):
        if v[i] == "plural":
            p = i
    res["plural"] = v[p+1]
    return res

# modificar
def adjParse(s):
    stk = []
    res = {}
    for c, i in zip(adjForms, range(2)):
        s = s.replace(c, str(i))
    v = s.split(" ")
    for i in v:
        if i in numbers:
            stk.append(i)
        else:
            for el in stk:
                res[verbForms[int(el)]] = i
            stk = []
    return res
