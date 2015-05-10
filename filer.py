import glob, os
import re

# needed global variables
# tv show library base dir
# baseDir of 

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]

def checkFolder(baseDir, folderName):
	pathExists = os.path.exists(baseDir+folderName+"/")
	if not pathExists:
		os.mkdir(baseDir+folderName)

def checkFolder(folderPath):
	pathExists = os.path.exists(folderPath)
	if not pathExists:
		os.mkdir(folderPath)

def placeFile(filePath,showTitle,libBaseDir):
	# check if Directory of showTitle exists
	checkFolder(libBaseDir, showTitle)

	# move the file to that directory
	fileName = os.path.basename(filePath)
#	os.rename(filePath,libBaseDir+"/"+showTitle+"/"+fileName)

	#check season number
	print fileName
	match = re.search(r'''(?ix)(?:s|S|^)\s*(\d{2})''',fileName)

	season = int(match.group(0)[1:3])
	checkFolder(libBaseDir+"/"+showTitle+"/", "Season "+ str(season))
	os.rename(filePath,libBaseDir+"/"+showTitle+"/"+"Season "+ str(season)+"/"+fileName)


def updateLibrary(showTitle,libBaseDir):
	cfiles = recursive_glob('./temp', '')
	fileSizes = []
	for cfile in cfiles:
		fileSizes.append(os.path.getsize(cfile))
	maxIndex = fileSizes.index(max(fileSizes))
	tvFile = cfiles[maxIndex]
	
	
	# move file to correct location
	placeFile(tvFile,showTitle,libBaseDir)
