import libtorrent as lt
import time, os
import filer

def downloadShowsToLibrary(magnetLinks, showTitles, tempDir, libBaseDir):
	newFiles = []
	for i in range(0,len(magnetLinks)):
		newFile = torrent(magnetLinks[i], showTitles[i], tempDir, libBaseDir)
		newFiles.append(newFile)
	return newFiles
def updateLibrary(info, showTitle, tempDir, libBaseDir):
        
    Nfiles = info.num_files()
    filePaths = []
    Sizes = []
    fileSizes = []
    for i in range(0,Nfiles):
            filePaths.append(tempDir + info.file_at(i).path)
    for cfile in filePaths:
            fileSizes.append(os.path.getsize(cfile))
    maxIndex = fileSizes.index(max(fileSizes))
    tvFile = filePaths[maxIndex]
    return filer.placeFile(tvFile,showTitle,libBaseDir) # return filepath of new item

def torrent(magnet, showTitle, tempDir, libBaseDir):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    filer.checkFolder(tempDir)
    print "Downloading " + showTitle
    params = {
        'save_path': tempDir,
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
    # download the torrent
    percent = 0
    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']
        #print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3' % \
        #            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
        #            s.num_peers, state_str[s.state], s.total_download/1000000)
        
        if percent < s.progress * 100:
            print str(percent) + " %"
            percent+=1
        #print s.progress * 100
        time.sleep(5)
    print "100%"
    print 'torrent downloaded, seeding to 3x...'
    # seed the torrent
    status = handle.status()
    timeStartSeed = time.time()
    while( 3 * status.total_download > status.total_upload ):
        status = handle.status()
        print str( float(status.total_upload) / (3 * status.total_download )) + "% seeded     Current Speed: " + str(status.upload_rate/1000)+"kb/s up"
        time.sleep(10)
        if time.time() - timeStartSeed > 10:  # seed for up to an hour
            break
    print "finished uploading"
    # return filepath of new item
    return updateLibrary(handle.get_torrent_info(), showTitle, tempDir ,libBaseDir) 
 
