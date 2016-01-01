import glob, os
import re, shutil
import subprocess
# needed global variables
# tv show library base dir
# baseDir of 


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
 
    #check season number of form S06, s04 ... etc
    match = re.search(r'''(?ix)(?:s|S|^)\s*(\d{2})''',fileName)
   
    # if no season number, just save in show title folder
    if match == None:
        newFilePath=libBaseDir+"/"+showTitle+"/"+fileName
        command="cp " + filePath + " " + newFilePath
        #subprocess.call(command,shell=True)
        #shutil.move(filePath, newFilePath)
        print "copying file to library..."
        shutil.copyfile(filePath, newFilePath)
        shutil.rmtree(os.path.dirname(filePath))
        print "copy done!"
        return newFilePath


    season = int(match.group(0)[1:3])
    checkFolder1(libBaseDir+"/"+showTitle+"/", "Season "+ str(season))
    
    newFilePath = libBaseDir+"/"+showTitle+"/"+"Season "+ str(season)+"/"+fileName
    #os.rename(filePath, newFilePath)
    #shutil.move(filePath, newFilePath)
    print "copying file to library..."
    #command="cp " + filePath + " " + newFilePath
    #subprocess.call(command,shell=True)
    shutil.copyfile(filePath, newFilePath)
    shutil.rmtree(os.path.dirname(filePath))
    print "copy done!"
    return newFilePath

