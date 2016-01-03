#! /usr/bin/env python
import torrenter, rss, filer #emailer
import shutil, os, time 
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--seed",
                  action="store_true", dest="seed", default=False,
                  help="seed to 3x")  # not yet implemented

(options, args) = parser.parse_args()

cwd		= os.getcwd()
baseDir 	= cwd + "/"
#tempDir		= cwd + "/temp/"
tempDir		= cwd + "/temp/"
#tempDir		= "/media/Seagate/temp/"
libBaseDir	= cwd+"/TVshows/"
#libBaseDir	= "/media/Seagate"+"/TVshows"
rssFeedURL = "http://showrss.info/rss.php?user_id=248153&hd=1&proper=1"

while(True):
    print "getting rss feed"
    rssFeed = rss.getRSSfeed(rssFeedURL)
    print "getting magnet links"
    updated, magnetLinks, showTitles = rss.update(rssFeed,tempDir,libBaseDir)
    if updated:
        print "found update - updating"
        newFilesPath = torrenter.downloadShowsToLibrary(magnetLinks, showTitles, tempDir, libBaseDir)
        newFiles = []
        for newFilePath in newFilesPath:
            newFiles.append(os.path.basename(newFilePath))
        #emailer.showUpdateEmail(newFiles)

# clean temp folder

    #break
    print "finished updating, sleeping..."	
    time.sleep(3600)
