#! /usr/bin/env python
import torrenter, rss, filer, emailer
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
#libBaseDir	= os.path.dirname(cwd)+"/TVshows/"
libBaseDir	= "/media/Seagate"+"/TVshows"

while(True):
    print "getting rss feed"
    rssFeed = rss.getRSSfeed()
    print "getting magnet links"
    updated, magnetLinks, showTitles = rss.update(rssFeed,tempDir,libBaseDir)
    if updated:
        print "found update - updating"
        newFilesPath = torrenter.downloadShowsToLibrary(magnetLinks, showTitles, tempDir, libBaseDir)
        newFiles = []
        for newFilePath in newFilesPath:
            newFiles.append(os.path.basename(newFilePath))
        emailer.showUpdateEmail(newFiles)

# clean temp folder

    #break	
    time.sleep(3600)
