##################################################################
## 			Anemone_1_OCR.py			##
##								##
##			 Conrad Spiteri				##
##			   29/10/2016				##
##								##
##################################################################
##OCRs bank statements into text files using ABBYY Cloud OCR SDK##
##################################################################
##								##
## ABBYY Cloud OCR Accont details can be changed from 		##
## AbbyyOnlineSdk.py lines 38 and 39.				##
## 								##
## To register for a free account go to http://ocrsdk.com/ 	##
##								##
##################################################################

print 'Starting...'

import subprocess, sys, os, glob, re

# Location of PDF files to convert
srcDocPath = '/home/pdf417/Dropbox/Projects/Anemone_1/PDFs/Statements/'
dstDocPath = '/home/pdf417/Dropbox/Projects/Anemone_1/Converted/Statements/'

# List of path contents
extention = '*.pdf'
targetExtention = '.txt'
directory = os.path.join(srcDocPath, extention)
files = glob.glob(directory)
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
files.sort(key=alphanum_key)
fileList = list(enumerate(files))

print len(fileList), "files to process in path ", directory

for i in range (len(fileList)):
	docToProcess = fileList[i][1]
	curDocName = docToProcess.split("/")[-1]
	outDocName = curDocName.split(".")[0] + targetExtention
	docToWrite = directory = os.path.join(dstDocPath, outDocName)
	print "Processing ", curDocName, "-->", outDocName
	cmd = 'python process.py ' + docToProcess + " " + docToWrite
	process = subprocess.call(cmd, shell=True)
	
print "Done."

