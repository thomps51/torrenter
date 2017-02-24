import glob, os
import re, shutil
import subprocess

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]
# bad naming... TODO: name the following functions better 

def checkFolder1(baseDir, folderName):
	pathExists = os.path.exists(baseDir+folderName+"/")
	if not pathExists:
		os.mkdir(baseDir+folderName)

def checkFolder(folderPath):
	pathExists = os.path.exists(folderPath)
	if not pathExists:
		os.mkdir(folderPath)

# can clean up
def placeFile(filePath,showTitle,libBaseDir):
    # check if Directory of showTitle exists
    checkFolder1(libBaseDir + "/", showTitle)
    
    # move the file to that directory
    fileName = os.path.basename(filePath)
 
    #check season number of form S06, s04 ... etc
    match = re.search(r'''(?ix)(?:s|S|^)\s*(\d{2})''',fileName)
   
    # if no season number, just save in show title folder
    if match == None:
        newFilePath=libBaseDir+"/"+showTitle+"/"+fileName
        command="cp " + filePath + " " + newFilePath
        shutil.move(filePath, newFilePath)
        print "copying file to library..."
        shutil.rmtree(os.path.dirname(filePath))
        print "copy done!"
        return newFilePath


    season = int(match.group(0)[1:3])
    checkFolder1(libBaseDir+"/"+showTitle+"/", "Season "+ str(season))
    
    newFilePath = libBaseDir+"/"+showTitle+"/"+"Season "+ str(season)+"/"+fileName
    print "copying file to library..."
    shutil.copyfile(filePath, newFilePath)
    shutil.rmtree(os.path.dirname(filePath))
    print "copy done!"
    return newFilePath

def updateLibrary(showTitle,libBaseDir):
    # kind of a hack, media file will have the largest filesize of downloaded files
	cfiles = recursive_glob('./temp', '')
	fileSizes = []
	for cfile in cfiles:
		fileSizes.append(os.path.getsize(cfile))
	maxIndex = fileSizes.index(max(fileSizes))
	tvFile = cfiles[maxIndex]
	
	# move file to correct location
	placeFile(tvFile,showTitle,libBaseDir)
