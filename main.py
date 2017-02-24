#! /usr/bin/env python
import torrenter, rss, filer #emailer
import shutil, os, time 
from optparse import OptionParser

# Configuration Options
cwd		= os.getcwd()
baseDir 	= cwd 
tempDir		= "/media/Seagate/TVshows/temp/"
libBaseDir	= "/media/Seagate"+"/TVshows"
#rssFeedURL  = "http://showrss.info/rss.php?user_id=248153&hd=1&proper=1"
rssFeedURL  = "http://showrss.info/user/67582.rss?magnets=true&namespaces=true&name=clean&quality=null&re=null"

# TODO : make seed option work, add option for sleep time, emailer
parser = OptionParser()
parser.add_option("-s", "--seed",
                  action="store_true", dest="seed", default=False,
                  help="seed to 3x")  # not yet implemented

(options, args) = parser.parse_args()


while(True):
    print "getting rss feed"
    rssFeed = rss.getRSSfeed(rssFeedURL)
    print "getting magnet links"
    updated, magnetLinks, showTitles = rss.update(rssFeed,tempDir,libBaseDir)
    if updated == None: # fix crashing on empty rss feed
        updated=False
    if updated:
        print "found update - updating"
        newFilesPath = torrenter.downloadShowsToLibrary(magnetLinks, showTitles, tempDir, libBaseDir)
        newFiles = []
        for newFilePath in newFilesPath:
            newFiles.append(os.path.basename(newFilePath))
# clean temp folder

    #break
    print "finished updating, sleeping..."	
    time.sleep(3600)
