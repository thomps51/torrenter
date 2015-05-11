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
	date  = rssFeed.entries[index].published[5:7]
	month = rssFeed.entries[index].published[8:11]
	year  = rssFeed.entries[index].published[12:16]
	
	t1 = rssFeed.entries[index].published[17:19]
	t2 = rssFeed.entries[index].published[20:22]
	t3 = rssFeed.entries[index].published[23:25]
	
	return datetime(int(year),int(Month(month)),int(date),int(t1),int(t2),int(t3))
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
	url = "http://showrss.info/rss.php?user_id=248153&hd=1&proper=1&raw=true" 
	d = feedparser.parse( url )
	return d


def getShowTitle(rssFeed, index):
	title = rssFeed.entries[index].title
	match = re.match(r'.+?(?= S\d\d)',title)
	return str(match.group(0))

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def update(rssFeed, tempDir, libBaseDir):
	#download latest
	updateTime = getDateRSS(rssFeed,0)
	for i in range(len(rssFeed.entries)-1,-1,-1): # start at oldest entry, work forward

		feedDate = getDateRSS(rssFeed, i)
		if getDateFile() < feedDate:
	
			# check from last item in RSS feed, comparing titles
			# if saved title not found, start from last item in feed
			print "updating! " + getShowTitle(rssFeed,i)
	
			
			magnet = rssFeed.entries[i].link
			torrenter.torrent(magnet, tempDir)	
			filer.updateLibrary(getShowTitle(rssFeed,i), libBaseDir)
		
	f = open('time.txt', 'w')
	f.write(str(updateTime))
	f.close()
