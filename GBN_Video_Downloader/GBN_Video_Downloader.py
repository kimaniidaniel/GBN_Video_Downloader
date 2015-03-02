#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------SETTINGS----------------------------
# Edit these settings as required
LOCALSTORE = "GBNNews/"                                     # directory to store downloaded videos
MAXPAGE = 15                                                # max number of pages to scan for videos
STARTPAGE = 0                                               # page to start scanning from
ARTICLES_PER_PAGE = 5                                       # expected articles on each page
BASEURL = "http://gbn.gd/en/gbnnews/1/?ls-art0="            # base URL to look for pages
PAGE_REGEX = "<a href=\"(/en/gbnnews/\d+/\d+\/.+\.htm)\">"  # regex used to find the respective pages for the articles eg <a href="/en/gbnnews/1/927/$2m-for-Home-Grown-Programme.htm">$2m for Home-Grown Programme</a>
VIDEO_REGEX = "<a href=\"(/attachment/\d+/.+\.mp4)"         # regex used to find the videos on the article pages
GBNSITE = "http://gbn.gd"                                   # GBN main site URL
#-------- END: Edit nothing under this line ---------------

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


class Downloader:
    """
    This downloads a page on the gbn.gd site
    """
    def getNewsFromPage(self, url):
        data = self.getWebPage(url)
        links = re.findall(PAGE_REGEX, data)                                                # Find all article links on page
        
        if len(links) > 1:
            distinctLinks = list(set(links))
            for x in range(0, len(distinctLinks)):                                          # Iterate through distinct links
                print ("Processing: %s" % distinctLinks[x])
                try:
                    data = self.getWebPage(GBNSITE + distinctLinks[x])
                except Exception as e:
                    self.logError(e)
                    continue

                links = re.findall(VIDEO_REGEX, data)                                       # Find the video link on the article page
                distinctLinks2 = list(set(links))

                for x in range(0, len(distinctLinks2)):                                     # Download each video on that page that's found above 
                    vid = distinctLinks2[x]
                    print ("\t- Downloading Video: %s" % vid)
                    filename = re.findall("/attachment/\d+/(.+.mp4)", vid)                  # Extract the file name from the video link
                    if not self.fileExists(LOCALSTORE + filename[0]):
                        if not os.path.exists(LOCALSTORE):                                  # Try to create the local directory if it's missing
                            try:
                                d = os.makedirs(LOCALSTORE)
                            except Exception as e:
                                self.logError(e)
                        
                        urlRequest.urlretrieve(GBNSITE + vid,LOCALSTORE + filename[0])      # Actual downloading of the video
                        print("\t- Saved: %s" % LOCALSTORE + filename[0])
                    else:
                          print("\t- File already exists") 
            print("Total: %d articles discovered\n" % len(distinctLinks))
    
    def logError(e):
        """
        Used to log all errors and display to screen
        """
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
        """
        Download a web page and return the bytes
        """
        return urlRequest.urlopen(url).read()

d = Downloader()
MAXPAGE +=1

print "Started: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
for x in range(STARTPAGE*ARTICLES_PER_PAGE,MAXPAGE*ARTICLES_PER_PAGE,ARTICLES_PER_PAGE):
    print("Page %d" % (x / ARTICLES_PER_PAGE))
    d.getNewsFromPage(BASEURL+str(x))
ts = time.time()
print "ENDED: " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
