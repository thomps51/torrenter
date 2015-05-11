#! /usr/bin/env python
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

	filer.checkFolder(tempDir)
	rss.update(rssFeed,tempDir,libBaseDir)
	shutil.rmtree(tempDir)
	break
	time.sleep(3600)
