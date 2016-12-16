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

# New Keyword Structure [[string], [length_range], [special_charracters], [type]].
# type = "num" for numeric only, "dec" for a number with decimal point, "alpNum" for alphanumeric string.

k0 = [["HSBC", "CrawfordTech Bank", "NatWest"], [0], [".",","], ["alpNum"]] # ko is a special instance that searches for the keyword only without extracting data related to it. Returns bank name.
k1 = [["Sort Code", "Branch Transit Number"], [6,6], ["-",":"], ["num"]]
k2 = [["Account Number"],[8,8],["-", ":"], ["num"]]
k3 = [["New Balance"],[3,8],[".", ","], ["dec"]]
t1 = ["BALANCE BROUGHT FORWARD", "Opening Balance", "BROUGHT FORWARD"]
t2 = ["BALANCE CARRIED FORWARD", "Closing Balance"]
HSBCkeywords = [k1,k2]
NATWkeywords = [k1,k2,k3]
transLims = [t1,t2]

# Establish the name of the bank
def getBankName(curmap, criteria):
        found = False; value = []
        string = criteria[0]; length = criteria[1]; specialChar = criteria[2]; criteriaType = criteria[3]
        cIdx = -1; c = -1
        for n, m in enumerate(iter(curmap.readline, "")):
                mm = m.lower().replace(" ", "")
                if len(mm) <= 0: # if empty line, ignore
                        continue
                for s in string:
                        ss = s.lower().replace(" ", "")				
                        for j in specialChar:
                                ss = ss.replace(j,'')
                                mm = mm.replace(j,'')
                        c = mm.find(ss)
                        if c >= 0:
                                return s

# Location of text files to convert
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
        value = {}; account = []
        docToProcess = fileList[i][1]
        curDocName = docToProcess.split("\\")[-1]
        with open(docToProcess,"r") as f:
                filemap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) #<= Windows Version, ### prot=mmap.PROT_READ) #<= Linux version
                bank = getBankName(filemap, k0)
###################################################### HSBC
                if bank == "HSBC":
                        import HSBC as hsbc
                        curDate = "01 Jan 2010"
                        print "\n\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                        print curDocName, "\nBank statement from -------> ", bank
                        for k in HSBCkeywords:
                                value = hsbc.getAccountDetails(filemap, k)
                                if len(value) > 0:
                                        account.append(value)
                                        print k[0], " -> ", value
                                else:
                                        print "ERROR ", k[0],  " not identified ", value
                        if account:
                                transactionListFile = dstDocPath + ''.join(str(l) for l in [account[0].replace("-",""),"_",account[1].replace("-",""),".txt"])
                                with open(transactionListFile, "a") as trannsactionFile:
                                        print "Extracting transactions...",
                                        transactions = hsbc.getTransactions(filemap, transLims)
                                        cleanTrans, curDate = hsbc.cleanTransactions(transactions, curDate)
                                        splitTrans = hsbc.identifyCRorDR(transactions,cleanTrans)
                                        for tr in splitTrans:
                                                #print '---'.join(tr)+"\n"
                                                trannsactionFile.write('?'.join(tr)+"\n")
                                print "Done."
                        else:
                                print "Account details not found."
                                break
###################################################### NATWEST                                
                elif bank == "NatWest":
                        import NATWEST as nw
                        curDate = "01 Jan 2010"
                        print "\n\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                        print curDocName, "\nBank statement from -------> ", bank
                        for k in NATWkeywords:
                                value = nw.getAccountDetails(filemap, k)
                                if len(value) > 0:
                                        if k is not NATWkeywords[-1]:
                                                account.append(value)
                                                print k[0], " -> ", value
                                else:
                                        print "ERROR ", k[0],  " not identified ", value
                        if account:
                                transactionListFile = dstDocPath + ''.join(str(l) for l in [account[0].replace("-",""),"_",account[1].replace("-",""),".txt"])
                                with open(transactionListFile, "a") as trannsactionFile:
                                        print "Extracting transactions..."
                                        transLims[-1].append(value)
                                        transactions = nw.getTransactions(filemap, transLims)
                                        cleanTrans, curDate = nw.cleanTransactions(transactions, curDate)
                                        splitTrans = nw.identifyCRorDR(transactions,cleanTrans)
                                        for tr in splitTrans:
                                                #print tr
                                                trannsactionFile.write('?'.join(tr)+"\n")
                                print "Done."
                        else:
                                print "Account details not found."
                                break
                else:
                        print "\n\nERROR - Bank not currently supported! \nStatement not processed. End\n"
        #if i > 0: break

print "\n\nProcessed ALL available files.\n"

