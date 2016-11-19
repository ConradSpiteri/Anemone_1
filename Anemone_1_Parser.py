##################################################################
## 			Anemone_1_Parser.py			##
##								##
##			 Conrad Spiteri				##
##			   29/10/2016				##
##								##
##################################################################
##  Extract and formats data contianed in the OCRed documents	##
##################################################################

import subprocess, sys, os, glob, re, time, mmap, contextlib
import findData_DEV as fKWD

# New Keyword Structure [[string], [length_range], [special_charracters], [type]].
# type = "num" for numeric only, "dec" for a number with decimal point, "alpNum" for alphanumeric string.

k0 = [["HSBC", "CrawfordTech Bank"], [0], [".",","], ["alpNum"]] # ko is a special instance that searches for the keyword only without extracting data related to it. Returns bank name.
k1 = [["Sort Code", "Branch Transit Number"], [6,6], ["-"], ["num"]]
k2 = [["Account Number"],[8,8],["-"], ["num"]]
t1 = ["BALANCE BROUGHT FORWARD", "Opening Balance"]
t2 = ["BALANCE CARRIED FORWARD", "Closing Balance"]
keywords = [k1,k2]
transLims = [t1,t2]

# Location of PDF files to convert
srcDocPath = 'C:\\Users\\Conrad\\Dropbox\\Projects\\Anemone_1\\Code\\Processed\\Statements\\'
dstDocPath = 'C:\\Users\\Conrad\\Dropbox\\Projects\\Anemone_1\\Code\\Converted\\Statements\\'

# List of path contents
extention = '*.txt'
directory = os.path.join(srcDocPath, extention)
files = glob.glob(directory)
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
files.sort(key=alphanum_key)
fileList = list(enumerate(files))

print len(fileList), "files to process."
for i in range (len(fileList)):
        value = {} #sortCode = []; accountNumber = []
        docToProcess = fileList[i][1]
        curDocName = docToProcess.split("/")[-1]
        #print "---------------------------", curDocName
        with open(docToProcess,"r") as f:
                filemap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                bank = fKWD.getBankName(filemap, k0)
                if bank:
                        print "\n\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                        print "Bank statement from -------> ", bank
                        for k in keywords:
                                value = fKWD.getAccountDetails(filemap, k)
                                if len(value) > 0:
                                        print k[0], " -> ", value
                                else:
                                        print "ERROR ", k[0],  " not identified ", value
                        transactions = fKWD.getTransactions(filemap, transLims)
                        print "\nTransactions for this statement: "
                        for tr in transactions:
                                print tr
                        print "End of Statement.\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                else:
                        print "\n\nERROR - Unidentified bank! \nStatement not processed. End\n"

print "\n\nDone.\n"

