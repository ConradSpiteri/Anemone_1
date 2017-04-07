##################################################################
## 			Anemone_1_Parser.py			##
##								##
##			 Conrad Spiteri				##
##			   29/10/2016				##
##								##
##################################################################
##  Extract and formats data contianed in the OCRed documents	##
##################################################################

import sys, os, glob, re, time, mmap, contextlib

bank = "HSBC"

if bank == "Lloyds":
        srcDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Processed\\Statements\\Lloyds_Transactions.csv'
        dstDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Converted\\Statements\\Lloyds_Transactions.txt'

        keysDict = {'C/P': 'CSH', 'CPT': 'CSH','DEB':'PAY','CHQ':'PAY','DD':'DDB','BGC':'DDB','FPO':'DDB','CHG':'DEB'}

        with open(srcDoc,"r") as f:
                with open(dstDoc, "a") as outF:
                        curmap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                        for n, curLine in enumerate(iter(curmap.readline, "")):
                                curLineRM = curLine.rstrip('\n').rstrip('\r')
                                splitLine = curLineRM.split(',')
                                if keysDict.has_key(splitLine[1]):
                                        if splitLine[3] > '':
                                                newLine = '?'.join([keysDict[splitLine[1]], splitLine[2].lower().replace("?","-"), '0', str(float(splitLine[3]))])
                                                
                                        else:
                                                newLine = '?'.join([keysDict[splitLine[1]], splitLine[2].lower().replace("?","-"), '1', str(float(splitLine[4]))])
                                        print newLine
                                        #outF.write(newLine+'\n')
                                else:
                                        print '"',splitLine[1],'"', 'key not found in line', n+1, '\n'
        f.close()
        outF.close()
elif bank == "FirstDirect":
        srcDocPath = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Processed\\Statements\\'
        dstDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Converted\\Statements\\FirstDirect_Transactions.txt'
        doneDocPath = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Processed\\Statements\\Extracted\\'

        # List of path contents
        extention = '*.CSV'
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
                docToMove = os.path.join(doneDocPath, curDocName)
 
                with open(docToProcess,"r") as f:
                        curmap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                        for n, curLine in enumerate(iter(curmap.readline, "")):
                                curLineRM = curLine.rstrip('\n').rstrip('\r')
                                splitLine = curLineRM.split(',')
                                if splitLine[2].lstrip()[0] == '-':
                                        newLine = '?'.join(['xxx', " ".join(splitLine[1].split()).lower().replace("?","-"), '0', splitLine[2].lstrip().lstrip('-')])
                                        print newLine
                                        #outF.write(newLine+'\n')
                                                        
                                else:
                                        try:
                                                float(splitLine[2])
                                                newLine = '?'.join(['xxx', " ".join(splitLine[1].split()).lower().replace("?","-"), '1', splitLine[2].lstrip().lstrip('-')])
                                                print newLine
                                                #outF.write(newLine+'\n')
                                        except:
                                                print '"',splitLine,'"', 'Error occoured in line', n+1, '\n'
                                                newLine = ''
                                #print newLine

        outF.close()

elif bank == "HSBC":
        srcDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Processed\\Statements\\midata5484b.csv'
        dstDoc = 'C:\\Users\\Conrad\\Google_Drive\\Other\\Anemone_1\\Code\\Converted\\Statements\\midata5484b.txt'

        keysDict = {'ATM': 'CSH','BP':'PAY','CHQ':'PAY','CIR':'CRD','CR':'CRD','DD':'DDB','DIV':'DIV','DR': 'DEB','MAE':'CRD','SO':'DDB','TRF':'PAY','VIS':'CRD',')))':'CRD'}

        with open(srcDoc,"r") as f:
                with open(dstDoc, "a") as outF:
                        curmap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                        for n, curLine in enumerate(iter(curmap.readline, "")):
                                curLineRM = curLine.rstrip('\n').rstrip('\r')
                                splitLine = curLineRM.split(',')
                                if keysDict.has_key(splitLine[1]):
                                        if len(splitLine) > 4:
                                                splitLine[3] = ''.join([splitLine[3].strip('"'),splitLine[4].strip('"')])
                                        if splitLine[3].lstrip()[0] == '-':
                                                newLine = '?'.join([keysDict[splitLine[1]], splitLine[2].lower().replace("?","-").replace('*','').replace('  ',' ').replace('  ',' '), '0', str(float(splitLine[3].lstrip().lstrip('-').strip(',')))])
                                                
                                        else:
                                                newLine = '?'.join([keysDict[splitLine[1]], splitLine[2].lower().replace("?","-").replace('*','').replace('  ',' ').replace('  ',' '), '1', str(float(splitLine[3].lstrip().lstrip('-').strip(',')))])
                                        print newLine                                                                   
                                        #outF.write(newLine+'\n')
                                                                   
                                else:
                                        print '"',splitLine[1],'"', 'key not found in line', n+1, '\n'
        f.close()
        outF.close()

print "\n\nDone.\n"

