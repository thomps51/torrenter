#! /usr/bin/env python
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

	filer.checkFolder(tempDir)
	rss.update(rssFeed,tempDir,libBaseDir)
	shutil.rmtree(tempDir)
	break
	time.sleep(3600)
