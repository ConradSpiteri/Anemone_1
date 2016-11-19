##################################################################
## 			findKeywordData.py			##
##								##
##			 Conrad Spiteri				##
##			   03/11/2016				##
##								##
##################################################################
##	Extract data based on keywords and their criteria	##
##################################################################
## New Keyword Structure [[string], [length_range], 		##
##	[special_charracters], [type]]. 			##
## type = "num" for numeric only, "dec" for a number with 	##
## decimal point, "alpNum" for alphanumeric string.		##
##################################################################

import subprocess, sys, os, glob, re, time, mmap, contextlib

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
					cIdx = m.find(s.lower())
					if cIdx < 0:
						cIdx = m.find(s.lower().replace(" ", ""))
					for searchStr in curLine:
						for i in range(length[1]-length[0]+1):
							repSpecial = searchStr.replace(' ','')
							for j in specialChar:
								repSpecial = repSpecial.replace(j,'')
							if all([repSpecial.isdigit(), len(repSpecial)==i+length[0]]):
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
		#m = ' '.join(m.split()).lower()
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
                                        break
                                
                        if found == True:
                                transactions.append([m.rstrip('\n').rstrip('\r')])
        return transactions
                        
                        
                        














        
