import feedparser
from datetime import datetime
import libtorrent as lt
import time
import sys
import re

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
def torrent(magnet):
	ses = lt.session()
	ses.listen_on(6881, 6891)
	params = {
	    'save_path': '/Users/tonythompson/RaspPi/temp',
	    'storage_mode': lt.storage_mode_t(2),
	    'paused': False,
	    'auto_managed': True,
	    'duplicate_is_error': True}
	
	handle = lt.add_magnet_uri(ses, magnet, params)
	ses.start_dht()
	print 'downloading metadata...'
	while (not handle.has_metadata()):
	    time.sleep(1)
	print 'got metadata, starting torrent download...'
	while (handle.status().state != lt.torrent_status.seeding):
	    s = handle.status()
	    state_str = ['queued', 'checking', 'downloading metadata', \
	                'downloading', 'finished', 'seeding', 'allocating']
#	    print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3' % \
#	                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#	                s.num_peers, state_str[s.state], s.total_download/1000000)
	    print s.progress * 100
	    time.sleep(5)	
	return

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

def update(rssFeed):
	# get date of late sync
	with open('time.txt', 'r') as f:
		sDate = f.readline()

	updated = False   # flag to tell if updated (used for filing)
	#download latest
	for i in range(0,len(rssFeed.entries)):

		if getDateFile() < getDateRSS(rssFeed, i):
	
			# check from last item in RSS feed, comparing titles
			# if saved title not found, start from last item in feed
			print "updating!"
	
			
			magnet = rssFeed.entries[0].link
			torrent(magnet)	
			f = open('time.txt', 'w')
			f.write(str(getDateRSS(rssFeed)))
			f.close()
			updated = True
		else:
			return updated
	
	
