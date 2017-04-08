##################################################################
## 		    Anemone_1_Lic_Parser.py			##
##								##
##			 Conrad Spiteri				##
##			   08/04/2017				##
##								##
##################################################################
##  Extract and formats data contianed in the OCRed documents	##
##################################################################

import sys, os, glob, re, time, mmap, contextlib
from dateutil.parser import parse


srcDocPath = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Processed\\Driving_Lic\\'
dstDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Converted\\Driving_Lic\\Details.txt'

# List of path contents
extention = '*.txt'
directory = os.path.join(srcDocPath, extention)
files = glob.glob(directory)
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
files.sort(key=alphanum_key)
fileList = list(enumerate(files))

outF = open(dstDoc, "a")
print len(fileList), "files to process."
for i in range (len(fileList)):
        docToProcess = fileList[i][1]
        curDocName = docToProcess.split("\\")[-1]
        addNext = 0
        with open(docToProcess,"r") as f:
                curmap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                for n, curLine in enumerate(iter(curmap.readline, "")):
                        curLineRM = curLine.rstrip('\n').rstrip('\r').lstrip()
                        if addNext == 1:
                            address = address + " " + curLineRM.lstrip().rstrip()
                            addNext = 2
                        if curLineRM[0:2] == '1.':
                            surname = curLineRM.replace('1.', '').lstrip().rstrip()
                        elif curLineRM[0:2] == '2.':
                            name = curLineRM.replace('2.', '').lstrip().rstrip()
                        elif curLineRM[0:2] == '3.':
                            dob_place = curLineRM.replace('3.', '').lstrip().rstrip().split()
                            dob = parse(dob_place[0]).strftime("%Y-%m-%d")
                            place = dob_place[1]
                        elif curLineRM[0:2] == '4a':
                            curLineRM = curLineRM.replace('4a.', '')
                            curLineRM = curLineRM.replace('4a', '')
                            lic_from = parse(curLineRM.replace('4a', '').lstrip().rstrip().split(' ')[0]).strftime("%Y-%m-%d")
                        elif curLineRM[0:2] == '4b':
                            curLineRM = curLineRM.replace('4b.', '')
                            curLineRM = curLineRM.replace('4b', '')
                            lic_to = parse(curLineRM.lstrip().rstrip().split(' ')[0]).strftime("%Y-%m-%d")
                        elif curLineRM[0:2] == '5.':
                            lic_no = curLineRM.replace('5.', '').lstrip().rstrip()
                        elif curLineRM[0:2] == '8.':
                            address = curLineRM.replace('8.', '').lstrip().rstrip()
                            addNext = 1

        print "Name        - ", name.lower()
        print "Surname     - ", surname.lower()
        print "Birth Date  - ", dob
        print "Place       - ", place
        print "Valid from  - ", lic_from
        print "Valid to    - ", lic_to
        print "Licence No. - ", lic_no
        print "Address     - ", address.replace(',', '').replace('.', '').lower()
        print
                        
outF.close()           
                        
                        
                            
                        
                            
