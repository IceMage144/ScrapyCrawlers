# Crawlers

## Available crawlers

* Wiki(1/2): A crawler that finds the conection between two wikipedia articles
* Text: A crawler that extracts the text from an wikipedia article

## Dictionaries

* dictionary.json was gotten from https://github.com/javierjulio/dictionary
* All conv.data were gotten from http://wordnet.princeton.edu/wordnet/download/current-version/ database

<!--
## Useful

egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z_]*\s" data.noun | cut -d ' ' -f 5 > conv.data.noun
https://docs.python.org/3/library/json.html
https://www.wordsapi.com/
https://doc.scrapy.org/en/latest/topics/selectors.html
http://www.thesaurus.com/
filename = 'wikipedia%s.txt' % response.url.split("/")[-1]
text = "".join(response.css("div.mw-content-ltr p").extract())  #extracting <p>s
text = re.sub("(<.*?>)|(\[.*?\])|(\{.*?\})", "", text) #extracting text
text = justify(text)
-->
