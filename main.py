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
	rss.update(rssFeed,tempDir)
	shutil.rmtree(tempDir)

	time.sleep(3600)
