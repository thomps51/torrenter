import feedparser
from datetime import datetime
import sys
import re
import filer
import torrenter

def Month(month):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    mon = months.index(month)
    return mon + 1
def getDateRSS(rssFeed , index):
    if index >= len(rssFeed.entries) or len(rssFeed.entries[0].published) < 26:
        print "Why did this happen? Index too large! Malformed rssFeed? Debug info:"
        print "Index = " + str(index)
        print "size of entries = " + len(rssFeed.entries)
        print "size of published = " + len(rssFeed.entries[0].published)
        print rssFeed.entries[0].published
        print rssFeed.entries[index].published 
    date  = rssFeed.entries[index].published[5:7]
    month = rssFeed.entries[index].published[8:11]
    year  = rssFeed.entries[index].published[12:16]
    
    #print date+month+year
    
    t1 = rssFeed.entries[index].published[17:19]
    t2 = rssFeed.entries[index].published[20:22]
    t3 = rssFeed.entries[index].published[23:25]
   
    dateRSS=datetime(int(year),int(Month(month)),int(date),int(t1),int(t2),int(t3))

    if dateRSS is None:
        print "Debug info:"
        print "Index = " + str(index)
        print "size of entries = " + len(rssFeed.entries)
        print "size of published = " + len(rssFeed.entries[0].published)
        print rssFeed.entries[0].published
        print rssFeed.entries[index].published 
 
    return dateRSS
# TODO: if no file avaiable, make new one
def getDateFile():
    with open('time.txt', 'r') as f:
        sDate = f.readline()
    
    year  = int(sDate[0:4])
    month = int(sDate[5:7])
    day   = int(sDate[8:10])
    t1    = int(sDate[11:13])
    t2    = int(sDate[14:16])
    t3    = int(sDate[17:19])
    return datetime(int(year),int(month),int(day),int(t1),int(t2),int(t3))

def getRSSfeed():
    #url = "http://showrss.info/rss.php?user_id=248153&hd=1&proper=1&raw=true" 
    #url = "http://kat.cr/usearch/The%20Late%20Show%20Colbert/?rss=1" 
    url = "http://showrss.info/rss.php?user_id=248153&hd=1&proper=1"
    d = feedparser.parse( url )
    return d


def getShowTitle(rssFeed, index):
    title = rssFeed.entries[index].title
    print title
    match = re.match(r'.+?(?= S\d\d)',title)
    if match == None:
        match = re.match(r'.+?(?= \dx\d\d)',title)
    if match == None:
        match = re.match(r'.+?(?= \d\d\d\d-\d\d-\d\d)',title)
    #print match
    #print str(match.group(0))
    return str(match.group(0))

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def update(rssFeed, tempDir, libBaseDir):
    #download latest
    updateTime  = getDateRSS(rssFeed,0)
    magnetLinks = []
    showTitles  = []
    updated	    = False
    for i in range(len(rssFeed.entries)-1,-1,-1): # start at oldest entry, work forward

        feedDate = getDateRSS(rssFeed, i)
        #print feedDate
        if getDateFile() < feedDate:
    	    # check from last item in RSS feed, comparing titles
    	    # if saved title not found, start from last item in feed
    	    print "Found Update: " + rssFeed.entries[i].title
    	    magnetLinks.append(rssFeed.entries[i].link)
    	    showTitles.append(getShowTitle(rssFeed,i))
    	    updated = True
    f = open('time.txt', 'w')
    f.write(str(updateTime))
    f.close()
    return updated, magnetLinks, showTitles
