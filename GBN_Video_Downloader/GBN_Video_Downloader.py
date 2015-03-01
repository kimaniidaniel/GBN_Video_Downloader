#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import time
import os
import io
import sys
print("GBN NEWS DOWNLOADER\nVersion 1.0")
print("Python Version: %s\n" % sys.version)

try:
    import urllib.request as urlRequest
except:
    import urllib as urlRequest


LOCALSTORE = "./GBNNews/"
MAXPAGE = 15
STARTPAGE = 0
ARTICLES_PER_PAGE = 5
BASEURL = "http://gbn.gd/en/gbnnews/1/?ls-art0="
PAGE_REGEX = "<a href=\"(/en/gbnnews/\d+/\d+\/.+\.htm)\">"
VIDEO_REGEX = "<a href=\"(/attachment/\d+/.+\.mp4)"

#<a href="/en/gbnnews/1/927/$2m-for-Home-Grown-Programme.htm">$2m for Home-Grown Programme</a>
class Downloader:
    """
    This downloads a page on the gbn.gd site
    """
    def getNewsFromPage(self, url):
        data = self.getWebPage(url)
        links = re.findall(PAGE_REGEX, data)                                                #Find all video links on page
        if len(links) > 1:
            distinctLinks = list(set(links))
            for x in range(0, len(distinctLinks)):
                print ("Processing: %s" % distinctLinks[x])
                try:
                    data = self.getWebPage("http://gbn.gd" + distinctLinks[x])
                except Exception as e:
                    self.logError(e)
                    continue
                links = re.findall(VIDEO_REGEX, data)
                distinctLinks2 = list(set(links))
                for x in range(0, len(distinctLinks2)):
                    vid = distinctLinks2[x]
                    print ("\t- Downloading Video: %s" % vid)
                    filename = re.findall("/attachment/\d+/(.+.mp4)", vid)
                    if not self.fileExists(LOCALSTORE + filename[0]):
                        if not os.path.exists(LOCALSTORE):
                            try:
                                d = os.makedirs(LOCALSTORE)
                            except Exception as e:
                                self.logError(e)
                        urlRequest.urlretrieve("http://gbn.gd" + vid,LOCALSTORE + filename[0])
                        print("\t- Saved: %s" % LOCALSTORE + filename[0])
                    else:
                          print("\t- File already exists") 
            print("Total: %d articles discovered\n" % len(distinctLinks))
    
    def logError(e):
        errorText = ""
        for x in e.args:
            errorText += " " + str(x)
        print("Unexpected error: ", errorText)
        
    def fileExists(self,file):
        return os.path.isfile(file)

    def progress_callback(blocks, block_size, total_size, d):
        #blocks->data downloaded so far (first argument of your callback)
        #block_size -> size of each block
        #total-size -> size of the file
        #implement code to calculate the percentage downloaded e.g
        print "downloaded %f%%" % blocks/float(total_size)
    
    def getWebPage(self,url):
        return urlRequest.urlopen(url).read()
        f = io.TextIOWrapper(page,encoding='utf-8')
        return page.read()

d = Downloader()
MAXPAGE +=1
ts = time.time()
print "Started: " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
for x in range(STARTPAGE*ARTICLES_PER_PAGE,MAXPAGE*ARTICLES_PER_PAGE,ARTICLES_PER_PAGE):
    print("Page %d" % (x / ARTICLES_PER_PAGE))
    d.getNewsFromPage(BASEURL+str(x))
ts = time.time()
print "ENDED: " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
