import re
#import requests
import os
import io
import sys
import urllib.request

LOCALSTORE = "/temp/videos/GBNNews/"
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
        #data = requests.get(url)
        data = self.getWebPage(url)
        links = re.findall("<a href=\"(/en/gbnnews/\d+/\d+\/.+\.htm)\">", data)
        if len(links) > 1:
            distinctLinks = list(set(links))
            for x in range(0, len(distinctLinks)):
                print ("Processing: %s" % distinctLinks[x])
                data = self.getWebPage("http://gbn.gd" + distinctLinks[x])
                links = re.findall("<a href=\"(/attachment/\d+/.+\.mp4)", data)
                distinctLinks2 = list(set(links))
                for x in range(0, len(distinctLinks2)):
                    vid = str.replace(distinctLinks2[x],'”','').replace('“','')
                    print ("\t- Downloading Video: %s" % vid)
                    filename = re.findall("/attachment/\d+/(.+.mp4)", vid)
                    if not self.fileExists(LOCALSTORE + filename[0]):
                        if not os.path.exists(LOCALSTORE):
                            try:
                                d = os.makedirs(LOCALSTORE)
                                print (d)
                                file = open(LOCALSTORE + filename[0], 'wb')
                                response = getWebPage("http://gbn.gd" + vid, stream=True)
                                for block in response.iter_content(1024):
                                    if not block:
                                        break
                                    file.write(block)
                                file.close()
                            except Exception as e:
                                print("Unexpected error: ",e.args[0])
                    else:
                          print("\t- File already exists") 
            print("Total: %d articles discovered\n" % len(distinctLinks))
    
    def fileExists(self,file):
        return os.path.isfile(file)
    
    def getWebPage(self,url):
        page = urllib.request.urlopen(url)
        f = io.TextIOWrapper(page,encoding='utf-8')
        return f.read()

d = Downloader()
for x in range(STARTPAGE,MAXPAGE*ARTICLES_PER_PAGE,ARTICLES_PER_PAGE):
    print("Page %d" % (x / ARTICLES_PER_PAGE))
    d.getNewsFromPage(BASEURL+str(x))

print("ALL DONE!")