import re
import requests
import os

LOCALSTORE = "/Users/kimaniidaniel/Desktop/GBNNews/"
MAXPAGE = 5
STARTPAGE = 3
ARTICLES_PER_PAGE = 5
BASEURL = "http://gbn.gd/en/gbnnews/1/?ls-art0="

#<a href="/en/gbnnews/1/927/$2m-for-Home-Grown-Programme.htm">$2m for Home-Grown Programme</a>
class Downloader:
    """
    This downloads a page on the gbn.gd site
    """
    def getNewsFromPage(self, url):
        data = requests.get(url)
        links = re.findall("<a href=\"(/en/gbnnews/\d+/\d+\/.+\.htm)\">", data.text)
        if len(links) > 1:
            distinctLinks = list(set(links))
            for x in range(0, len(distinctLinks)):
                print ("Processing: %s" % distinctLinks[x])
                data = requests.get("http://gbn.gd" + distinctLinks[x])
                links = re.findall("<a href=\"(/attachment/\d+/.+\.mp4)", data.text)
                distinctLinks2 = list(set(links))
                for x in range(0, len(distinctLinks2)):
                    print (distinctLinks2[x])
                    print ("\t- Downloading Video: %s" % distinctLinks2[x])
                    filename = re.findall("/attachment/\d+/(.+.mp4)", distinctLinks2[x])
                    if self.fileExists(LOCALSTORE + filename[0]) == False:
                        file = open(LOCALSTORE + filename[0], 'wb')
                        response = requests.get("http://gbn.gd" + distinctLinks2[x], stream=True)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            file.write(block)
                        file.close()
                    else:
                          print("\t- File already exists") 
            print("Total: %d articles discovered\n" % len(distinctLinks))
    
    def fileExists(self,file):
        return os.path.isfile(file)

d = Downloader()
for x in range(STARTPAGE,MAXPAGE*ARTICLES_PER_PAGE,ARTICLES_PER_PAGE):
    print("Page %d" % (x / ARTICLES_PER_PAGE))
    d.getNewsFromPage(BASEURL+str(x))

print("ALL DONE!")