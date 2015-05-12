#! /usr/bin/env python
import torrenter
import rss
import filer
import shutil, os, time 
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--seed",
                  action="store_true", dest="seed", default=False,
                  help="seed to 3x")

(options, args) = parser.parse_args()

cwd		= os.getcwd()
baseDir 	= cwd + "/"
tempDir		= cwd + "/temp/"
libBaseDir	= os.path.dirname(cwd)+"/TVshows/"

while(True):
	rssFeed = rss.getRSSfeed()

	magnetLinks, showTitles = rss.update(rssFeed,tempDir,libBaseDir)
	newFiles = torrenter.downloadShowsToLibrary(magnetLinks, showTitles, tempDir, libBaseDir)	
	print newFiles	
	# clean temp folder
	
	break
	time.sleep(3600)
