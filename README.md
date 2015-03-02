# GBN Video Downloader

This project came from the need to get news onto my XBMC media player. 
There were no current plugins that allowed me to watch local news and I had no interest in creating a plugin. So the next best thing was to create this script that allowed
me to download the videos of their public site. Once the settings are configured on the script and it's scheduled using cron or windows scheduler it does it's job well.

The script contains all the settings on the top lines. Here they are with some notes
```sh
----------------------SETTINGS----------------------------
LOCALSTORE = "GBNNews/"                                     # directory to store downloaded videos
MAXPAGE = 15                                                # max number of pages to scan for videos
STARTPAGE = 0                                               # page to start scanning from
ARTICLES_PER_PAGE = 5                                       # expected articles on each page
BASEURL = "http://gbn.gd/en/gbnnews/1/?ls-art0="            # base URL to look for pages
PAGE_REGEX = "<a href=\"(/en/gbnnews/\d+/\d+\/.+\.htm)\">"  # regex used to find the respective pages for the articles eg <a href="/en/gbnnews/1/927/$2m-for-Home-Grown-Programme.htm">$2m for Home-Grown Programme</a>
VIDEO_REGEX = "<a href=\"(/attachment/\d+/.+\.mp4)"         # regex used to find the videos on the article pages
GBNSITE = "http://gbn.gd"                                   # GBN main site URL
-------- END: Edit nothing under this line ---------------
```
Once those are set properly the script can be execured via the shell
