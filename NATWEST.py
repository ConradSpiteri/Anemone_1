##################################################################
## 			findData.py     			##
##								##
##			 Conrad Spiteri				##
##			   07/12/2016				##
##								##
##################################################################
##	Extract data based on keywords and their criteria	##
##################################################################


import sys, os, glob, re, time, mmap, contextlib
from dateutil.parser import parse

					
# Search for a number based on keyword criteria
def getAccountDetails(curmap, criteria): 
	nextLineRequired = False; found = False; value = []
	#parse keyword criteria
	string = criteria[0]; length = criteria[1]; specialChar = criteria[2]; criteriaType = criteria[3]
	for s in string:
		if found == True:
			return value
		#print "current search = ", s
		nextLineRequired = False; found = False; value = []
		curmap.seek(0)
		for n, m in enumerate(iter(curmap.readline, "")):
			m = ' '.join(m.split()).lower()
			if len(m) <= 0: # if empty line, ignore
				continue
			#print m
			curLine = m.split()
			if nextLineRequired == True:
				for searchStr in curLine:
					for i in range(length[1]-length[0]+1):
						repSpecial = searchStr
						for j in specialChar:
							repSpecial = repSpecial.replace(j,'')
						if all([repSpecial.isdigit(), len(repSpecial)==i+length[0]]):
							value = searchStr
							found = True
							nextLineRequired = False
							return value
						else:
							nextLineRequired = False		
			elif found == False:
				mm = m.replace(" ", "")
				c = mm.find(s.lower().replace(" ", ""))
				if c >= 0:
                                        #print mm[c:]
					cIdx = m.find(s.lower())
					if cIdx < 0:
						cIdx = m.find(s.lower().replace(" ", ""))
					for searchStr in curLine:
						for i in range(length[1]-length[0]+1):
							repSpecial = re.sub('[^0-9a-zA-Z]+', '', searchStr) #searchStr.replace(' ','')
							#for j in specialChar:
							#	repSpecial = repSpecial.replace(j,'')
							# print repSpecial, repSpecial.isdigit(), len(repSpecial), i+length[0]
							if all([repSpecial.isdigit(), len(repSpecial)==i+length[0]]):
                                                                if criteriaType[0] == "dec":
                                                                        value = re.sub('[^0-9,.]+', '', searchStr)
                                                                else:
                                                                        value = searchStr
								found = True
								nextLineRequired = False
								return value
							else:
								nextLineRequired = True		
			cIdx = -1; c = -1
	return value

def getTransactions(curmap, limitKeyWords):
        transactions = []; found = False; t1 = limitKeyWords[0]; t2 = limitKeyWords[1] # t1 = start of transactions keyword; t2 = end of transactions keyword.
        for n, m in enumerate(iter(curmap.readline, "")):
                c = -1
		#m = ' '.join(m.split()).lower()                        # if uncommented will remove all spaces and hence loose column formating
		if found == False:
                        mm = m.lower().replace(" ", "")
                        if len(m) <= 0: # if empty line, ignore
                                continue
                        for s1 in t1:
                                ss = s1.lower().replace(" ", "")				
                                c = mm.find(ss)
                                if c >= 0:
                                        found = True                    # found start of transactions keyword
                                        break
                elif found == True:                                     
                        mm = m.lower().replace(" ", "")
                        if len(mm) <= 0: # if empty line, ignore
                                continue
                        for s2 in t2:
                                ss = s2.lower().replace(" ", "")				
                                c = mm.find(ss)
                                if c >= 0:
                                        found = False                   # found end of transactions keyword
                                        temps2 = re.sub('[^0-9a-zA-Z]+', '', s2)
                                        if temps2.isdigit():
                                                transactions.append([m.rstrip('\n').rstrip('\r').rstrip().lstrip()])
                                        break          
                        if found == True:
                                transactions.append([m.rstrip('\n').rstrip('\r').rstrip().lstrip()])
        return transactions


def cleanTransactions(transactions, curDate):
        keys = ['interest', 'online transaction', 'atm transaction', 'direct debit', 'charges', 'automated credit'] # HSBC Transaction definition codes
        cleanTr = []; found = False; space = "   "; transCodeField = []
        for tr in transactions:
                curLine = " " + ' '.join(tr[0].lstrip().split())
                cc = curLine.replace(" ", "")
                if len(cc) <= 0: # if empty line, ignore
                        continue
                try:                                                                            # check for date field within the first 10 characters (ommiting leading spaces)
                        curDate = parse(tr[0][:13].lstrip().rstrip())
                        dateMissing = False
                except:
                        dateMissing = True
                if found == False:                                                              # first instance of running the code - build the transaction line
                        #any(substring in string for substring in substring_list)
                        if  any(key in tr[0].lower() for key in keys):                          #transCodeField in keys: #
                                if dateMissing == False:
                                        curTr = curDate.strftime("%Y-%m-%d") + space + tr[0][13:].lstrip()
                                else:
                                        if type(curDate).__name__ is not 'datetime.datetime':
                                                curDate = parse(curDate)
                                        curTr = curDate.strftime("%Y-%m-%d") + space + tr[0].lstrip()
                                found = True
                else:                                                                           # all other runs - append to current transaction or start a new one
                        if any(key in tr[0].lower() for key in keys):                           # transCodeField in keys: ### if another key is found in the current line, then previous line is a complete transaction
                                cleanTr.append(curTr[:10] + space + curTr[10:].lstrip()) # save previous transaction
                                if dateMissing == False:
                                        curTr = curDate.strftime("%Y-%m-%d") + space + tr[0][13:].lstrip()
                                else:
                                        curTr = curDate.strftime("%Y-%m-%d") + space + tr[0].lstrip()
                        #else:                                                   # if no key found then current line part of current transaction. Concatinate
                                #curTr = curTr + " " + tr[0].lstrip()
        cleanTr.append(curTr[:10] + space + curTr[10:].lstrip())
        return cleanTr, curDate

def identifyCRorDR(transactions, cleanTr):
        splitTr = []; posDR = 0; count = 0; transWithVal = []
        keysDict = {'atm transaction':'CSH','online transaction':'PAY','CHQ':'PAY','CIR':'CAR','automated credit':'CRD','direct debit':'DDB','interest':'DIV','charges':'DEB','MAE':'CRD','SO':'STO','TRF':'TRF','VIS':'CRD',')))':'CRD'}
        # Calculate average end location for debit transactions based on variance from start of description
        for tr in transactions:                 
                tempTr = re.split(r'\s{2,}',tr[0])

                try:                                    # line has both transation value and balance
                        float(tempTr[-2].replace(",", ""))
                        valueTr = tempTr[-2].lstrip().rstrip()
                        desc = tempTr[-3].lstrip().rstrip()
                except:
                        try:                            # line has transation value only
                                float(tempTr[-1].replace(",", ""))
                                valueTr = tempTr[-1].lstrip().rstrip()
                                desc = tempTr[-2].lstrip().rstrip()
                        except:              # line has neither transation value or balance (highly unlikely)
                                continue
                posDesc = tr[0].find(desc)
                posVal = tr[0].find(valueTr) + len(valueTr)
                posDR += (posVal-posDesc)
                count += 1
                transWithVal.append(tr[0][posDesc:posVal])
        avgPosVal = (posDR/count) + 4

        # Determine whether transaction is debit or credit depending on position with respect to average end location for debit transactions calculated above
        for tr in cleanTr:
                tempTr = re.split(r'\s{2,}',tr)
                try:                                    # line has both transation value and balance
                        tempVal = float(tempTr[-2].replace(",", ""))
                        valueTr = '%.2f' % tempVal
                        desc = '{0:<50.50}'.format(tempTr[2].lstrip().rstrip())
                except:
                        try:                            # line has transation value only
                                tempVal = float(tempTr[-1].replace(",", ""))
                                valueTr = '%.2f' % tempVal
                                desc = '{0:<50.50}'.format(tempTr[2].lstrip().rstrip())
                        except:                         # line has neither transation value or balance (highly unlikely)
                                continue
                if len(transWithVal)>0:
                        for tWV in  transWithVal:                 
                                tempTWV = re.split(r'\s{2,}',tWV)
                                if tr.find(tWV) >= 0:
                                        if tempTr[1].lower() in keysDict:
                                                curKey = keysDict[tempTr[1].lower()]
                                        else:
                                                curKey = 'UNK'
                                        if (tWV.find(tempTWV[-1]) + len(tempTWV[-1])) < avgPosVal:                                                
                                                splitTr.append([tempTr[0],curKey, ' '.join(desc.split()).lower(),"1",valueTr.replace(",", "")])
                                        else:
                                                splitTr.append([tempTr[0],curKey, ' '.join(desc.split()).lower(),"0",valueTr.replace(",", "")])
                                        transWithVal.remove(tWV)
                                        break
        return splitTr
                                                
                        
                












        
                                
