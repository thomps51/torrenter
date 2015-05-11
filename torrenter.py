import libtorrent as lt
import time

def torrent(magnet , tempDir):
        ses = lt.session()
        ses.listen_on(6881, 6891)
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
        while (handle.status().state != lt.torrent_status.seeding):
            s = handle.status()
            state_str = ['queued', 'checking', 'downloading metadata', \
                        'downloading', 'finished', 'seeding', 'allocating']
#           print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3' % \
#                       (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#                       s.num_peers, state_str[s.state], s.total_download/1000000)
            print s.progress * 100
            time.sleep(5)
	print 'torrent downloaded, seeding to 3x...'
	# seed the torrent
	seeded = False
	status = handle.status()
	while( 3 * status.total_download > status.total_upload ):
		status = handle.status()
		print str( float(status.total_upload) / (3 * status.total_download )) + "% seeded     Current Speed: " + str(status.upload_rate/1000)+"kb/s up"
		time.sleep(10)
        return
