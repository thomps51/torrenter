import rss
import filer
import shutil
import os
import time

cwd		= os.getcwd()
baseDir 	= cwd + "/"
tempDir		= cwd + "/temp/"
libBaseDir	= os.path.dirname(cwd)+"/TVshows/"


while(True):
	rssFeed = rss.getRSSfeed()
	showTitle = rss.getShowTitle(rssFeed,0)
	
	filer.checkFolder(tempDir)
	updated = rss.update(rssFeed)
	if updated:
		filer.updateLibrary(showTitle,libBaseDir)
	shutil.rmtree(tempDir)
	time.sleep(3600)
