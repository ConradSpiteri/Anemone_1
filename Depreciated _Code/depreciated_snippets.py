def getSortCode(curmap):
	nextLineRequiredSC = False; foundSC = False; sortCode = []
	for n, m in enumerate(iter(curmap.readline, "")):
		if foundSC == True:
			break
		m = ' '.join(m.split()).lower()
		if len(m) <= 0:
			continue
		curLine = m.split()
		#------------------------------- Find SortCode and extract it
		if nextLineRequiredSC == True:
			for scSearch in curLine:
				if all([scSearch.replace('-','').isdigit(), len(scSearch.replace('-',''))==6]):
					sortCode = scSearch
					foundSC = True
					nextLineRequiredSC = False
				else:
					nextLineRequiredSC = False		
		elif foundSC == False:
			mm = m.replace(" ", "")				
			sc = mm.find(SC_)
			if sc >= 0:
				scIdx = m.find(SC)
				if scIdx < 0:
					scIdx = m.find(SC_)
				#print n, scIdx, m[scIdx:scIdx+len(SC)],
				for scSearch in curLine:
					if all([scSearch.replace('-','').isdigit(), len(scSearch.replace('-',''))==6]):
						sortCode = scSearch
						foundSC = True
						nextLineRequiredSC = False
					else:
						nextLineRequiredSC = True
		scIdx = -1; sc = -1	
	return sortCode

def getAccNumber(curmap):
	nextLineRequiredACC = False; foundACC = False; accountNum = []
	for n, m in enumerate(iter(curmap.readline, "")):
		if foundACC == True:
			break
		m = ' '.join(m.split()).lower()
		if len(m) <= 0:
			continue
		curLine = m.split()
		#------------------------------- Find Acount Number and extract it
		if nextLineRequiredACC == True:
			for accSearch in curLine:
				if all([accSearch.replace('-','').isdigit(), len(accSearch.replace('-',''))==8]):
					accountNum = accSearch
					foundACC = True
					nextLineRequiredACC = False
				else:
					nextLineRequiredACC = False		
		elif foundACC == False:
			mm = m.replace(" ", "")				
			acc = mm.find(ACC_)
			if acc >= 0:
				accIdx = m.find(ACC)
				if accIdx < 0:
					accIdx = m.find(ACC_)
				#print n, accIdx, m[accIdx:accIdx+len(ACC)],
				for accSearch in curLine:
					if all([accSearch.replace('-','').isdigit(), len(accSearch.replace('-',''))==8]):
						accountNum = accSearch
						foundACC = True
						nextLineRequiredACC = False
					else:
						nextLineRequiredACC = True		
		accIdx = -1; acc = -1
	return accountNum


# Keywords
BBF = "BALANCE BROUGHT FORWARD".lower(); BBF_ = BBF.replace(" ", "")
SC  = "Sort Code".lower(); SC_ = SC.replace(" ", "")
ACC = "Account Number".lower(); ACC_ = ACC.replace(" ", "")
