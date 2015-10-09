import glob, os
import re, shutil
import subprocess
# needed global variables
# tv show library base dir
# baseDir of 

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]

def checkFolder1(baseDir, folderName):
	pathExists = os.path.exists(baseDir+folderName+"/")
	if not pathExists:
		os.mkdir(baseDir+folderName)

def checkFolder(folderPath):
	pathExists = os.path.exists(folderPath)
	if not pathExists:
		os.mkdir(folderPath)

def placeFile(filePath,showTitle,libBaseDir):
    # check if Directory of showTitle exists
    checkFolder1(libBaseDir + "/", showTitle)
    
    # move the file to that directory
    fileName = os.path.basename(filePath)
    #os.rename(filePath,libBaseDir+"/"+showTitle+"/"+fileName)
    #shutil.move(filePath, libBaseDir+"/"+showTitle+"/"+fileName)
   
    if "Stephen Colbert" in showTitle:
        newFilePath=libBaseDir+"/"+showTitle+"/"+fileName
        command="cp " + filePath + " " + newFilePath
        #subprocess.call(command,shell=True)
        #shutil.move(filePath, newFilePath)
        shutil.copyfile(filePath, newFilePath)
        return newFilePath
 
    #check season number
    match = re.search(r'''(?ix)(?:s|S|^)\s*(\d{2})''',fileName)
    
    season = int(match.group(0)[1:3])
    checkFolder1(libBaseDir+"/"+showTitle+"/", "Season "+ str(season))
    
    newFilePath = libBaseDir+"/"+showTitle+"/"+"Season "+ str(season)+"/"+fileName
    #os.rename(filePath, newFilePath)
    #shutil.move(filePath, newFilePath)
    print "copying file to library..."
    #command="cp " + filePath + " " + newFilePath
    #subprocess.call(command,shell=True)
    shutil.copyfile(filePath, newFilePath)
    print "copy done!"
    return newFilePath

def updateLibrary(showTitle,libBaseDir):
	cfiles = recursive_glob('./temp', '')
	fileSizes = []
	for cfile in cfiles:
		fileSizes.append(os.path.getsize(cfile))
	maxIndex = fileSizes.index(max(fileSizes))
	tvFile = cfiles[maxIndex]
	
	
	# move file to correct location
	placeFile(tvFile,showTitle,libBaseDir)
