########################################################################################################################
## 		                                      Anemone_1_Trainer.py	                                      ##
##                                                      							      ##
## 		                                          Conrad Spiteri				              ##
## 		                                            08/12/2016				                      ##
##                                                      							      ##
########################################################################################################################
##                                      Learns classification of transactions from dataset	                      ##
########################################################################################################################

import sys, os, glob, re, time, mmap, contextlib, random
import nltk
from tabulate import tabulate

########################################################################################################################
# Constants                                                                                                            #
########################################################################################################################
srcDocPath = 'C:\\Users\\Conrad\\Dropbox\\Projects\\Anemone_1\\Code\\Converted\\Classified\\'
dstDocPath = 'C:\\Users\\Conrad\\Dropbox\\Projects\\Anemone_1\\Code\\Converted\\Results\\'
classDesc = []
testDataPercentage = 10                     # Percentage of data to use for testing after training
trainingThreshold =  0.0015                 # 0.00255
confThreshold = 80                          # Confidence threshold level
trainStepThresholdMax = 50
trainStepThresholdMin = 5
hiddenLayer0neurons = 631
hiddenLayer1neurons = 601
classificationType = ['Food', 'Cash', 'Monthly Payment', 'Travel', 'Leisure', 'Miscellaneous']


########################################################################################################################
# flatten - construct for nltk to undimentionalize the data. NLTK requiremet                                           #
########################################################################################################################
def flatten(seq,container=None):
    if container is None:
        container = []
    for s in seq:
        if hasattr(s,'__iter__'):
            flatten(s,container)
        else:
            container.append(s)
    return container


########################################################################################################################
# loadTrainingData - Loads and tokenizes the training data and divides it into training and testing datasets           #
########################################################################################################################
def loadTrainingData():
    fullTransactions = []
    trainingData = []
    extention = '*.txt'
    directory = os.path.join(srcDocPath, extention)
    files = glob.glob(directory)
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    files.sort(key=alphanum_key)
    fileList = list(enumerate(files))
    maxlen = 0

    for i in range (len(fileList)):
        docToProcess = fileList[i][1]
        curDocName = docToProcess.split("\\")[-1]
        #print "Processing ", curDocName, "..."
        f = open(docToProcess,"r")
        for i, curLine in enumerate(f):             # LOAD DATA AND SPLIT INTO TRAINING AND TEST SAMPLES
            curLine = curLine.rstrip('\n').rstrip('\r').split("\t")
            fullTransactions.append([i]+curLine)
            text = nltk.word_tokenize('{0:<50.50}'.format(curLine[2]))
            trainingData.append([i,['{0:<100.100}'.format(' '.join(flatten([curLine[1],nltk.pos_tag(text)]))),curLine[3]],curLine[5]])
            if trainingData[-1][1][0] > maxlen:
                   maxlen = len(trainingData[-1][1][0])
        testData = random.sample(trainingData, len(trainingData)/testDataPercentage)
        for item in testData:
            trainingData.remove(item)
    f.close()
    return trainingData, testData

########################################################################################################################
# buildNN2HiddenLayer - construct a feed forward ANN with 2 hidden layers and return a pointer to the network          #
########################################################################################################################
def buildNN2HiddenLayer(trnData, netNo):
    from pybrain.structure import FeedForwardNetwork, RecurrentNetwork
    from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer, SoftmaxLayer
    from pybrain.structure import FullConnection
    
    n = FeedForwardNetwork()
    inLayer = LinearLayer(trnData.indim)                                        # Define Layer Types
    if netNo == 1 or netNo == 3:
        hiddenLayer0 = TanhLayer(hiddenLayer0neurons)                               # Tanh      
        hiddenLayer1 = SigmoidLayer(hiddenLayer1neurons)                            # Sigmoid
    elif netNo == 2:
        hiddenLayer0 = TanhLayer(hiddenLayer1neurons)                               # Tanh      
        hiddenLayer1 = SigmoidLayer(hiddenLayer0neurons)                            # Sigmoid
    
    outLayer = SoftmaxLayer(trnData.outdim)                                     # SoftmaxLayer

    n.addInputModule(inLayer)
    n.addModule(hiddenLayer0)
    n.addModule(hiddenLayer1)
    n.addOutputModule(outLayer)
    
    in_to_hidden0 = FullConnection(inLayer, hiddenLayer0)                       # Define connections
    hidden0_to_hidden1 = FullConnection(hiddenLayer0, hiddenLayer1)
    hidden1_to_out = FullConnection(hiddenLayer1, outLayer)
    n.addConnection(in_to_hidden0)
    n.addConnection(hidden0_to_hidden1)
    n.addConnection(hidden1_to_out)
    n.sortModules()
    return n


########################################################################################################################
# buildDataSet - construct the dataset as required by pybrain and return a pointer to the dataset                      #
########################################################################################################################
def buildDataSet(inp):
    from pybrain.datasets import ClassificationDataSet
    DS = ClassificationDataSet(len(' '.join(inp[0][1])),1, nb_classes=len(classificationType))                 
    for i in range(len(inp)):
        disseminated = map(lambda c: ord(c), ' '.join(inp[i][1]))
        # print i, disseminated, len(disseminated)
        DS.addSample(disseminated,classificationType.index(inp[i][2]))
    DS._convertToOneOfMany()
    return DS


########################################################################################################################
# trainANnNetwork - Train the ANN until error is below threshold or number of steps reached                            #
########################################################################################################################
def trainANnNetwork(netw,dataSet,no):
    from pybrain.supervised.trainers import BackpropTrainer
    if no == 1: weightDec = 0.005
    if no == 2: weightDec = 0.005
    if no == 3: weightDec = 0.005
    vbose=False
    errList = []
    trainer = BackpropTrainer(netw, dataset=dataSet, verbose=vbose, momentum=0.1, weightdecay=weightDec)
    counter = 0; err = 10000
    print "Training network",no,"... Please wait...",
    while ((err > trainingThreshold or counter <= trainStepThresholdMin) and counter <= trainStepThresholdMax):
        tempErr = trainer.train()
        errList.append(tempErr*100)
        if tempErr < err:
            #if vbose == False: print counter+1, "\t : ", tempErr
            err = tempErr                                        # use tempErr to exit when threshold is reached or 10000 to go through all epochs
        counter += 1
    if vbose == False: print "Network Training error of", tempErr, "after", counter-1, "steps"
    return netw, errList

########################################################################################################################
# liveRun - Generates an output based on the new input data                                                            #
########################################################################################################################
def liveRun(net,dataSet):
    net.sortModules()
    retValues = net.activate(dataSet)
    highest = -1.0; classVal = -1.0; secHighest = -1.0; classVal2nd = -1.0
    for j in range(len(retValues)):
        if retValues[j] >= highest:
            classVal = j
            highest = retValues[j]
    return retValues, classVal


########################################################################################################################
# Main
########################################################################################################################

print "Loading DataSet ..."
trainDS, testDS = loadTrainingData()                              # Load and split dataset
trainDataSet = buildDataSet(trainDS)
testDataSet = buildDataSet(testDS)

print "Building Neural Networks ..."
net1 = buildNN2HiddenLayer(trainDataSet,1)                                    # Build FF,MLP,ANN networks with 2 hidden layers
net2 = buildNN2HiddenLayer(trainDataSet,2)
net3 = buildNN2HiddenLayer(trainDataSet,3)

net1, progress1 = trainANnNetwork(net1,trainDataSet,1)                   # Train the networks
net2, progress2 = trainANnNetwork(net2,trainDataSet,2)
net3, progress3 = trainANnNetwork(net3,trainDataSet,3)

print "Testing the classifier ..."

table = []
headers=['Designated', 'Classified', 'Comment', 'Confidence', 'ANN1', 'ANN2', 'ANN3', 'Majority']

for v in range(len(testDataSet['input'])):
    values1, classVal1 = liveRun(net1,testDataSet['input'][v])
    values2, classVal2 = liveRun(net2,testDataSet['input'][v])
    values3, classVal3 = liveRun(net3,testDataSet['input'][v])
    
    if classVal1 == classVal2 and classVal1 == classVal3:
        if classVal1 == classificationType.index(testDS[v][2]):
            labelX = ""
        else:
            labelX = " XXX"
        confidence = int((values1[classVal1]+values2[classVal2]+values3[classVal3])/3*100)
        if confidence < confThreshold:
            labelX = labelX + " LOW CONFIDENCE"
        tLine = v+1, testDS[v][2], classificationType[classVal1], labelX, confidence, values1[classVal1], values2[classVal2], values3[classVal3], " - 1,2,3"
        table.append(tLine)
    elif classVal1 == classVal2 and classVal1 != classVal3:
        if classVal1 == classificationType.index(testDS[v][2]):
            labelX = ""
        else:
            labelX = " XXX"
        confidence = int((values1[classVal1]+values2[classVal1]+values3[classVal1])/3*100)
        if confidence < confThreshold:
            labelX = labelX + " LOW CONFIDENCE"
        tLine = v+1, testDS[v][2], classificationType[classVal1], labelX, confidence, values1[classVal1], values2[classVal2], values3[classVal3], " - 1,2"
        table.append(tLine)
    elif classVal1 == classVal3 and classVal1 != classVal2:
        if classVal1 == classificationType.index(testDS[v][2]):
            labelX = ""
        else:
            labelX = " XXX"
        confidence = int((values1[classVal1]+values2[classVal1]+values3[classVal1])/3*100)
        if confidence < confThreshold:
            labelX = labelX + " LOW CONFIDENCE"
        tLine = v+1, testDS[v][2], classificationType[classVal1], labelX, confidence, values1[classVal1], values2[classVal2], values3[classVal3], " - 1,3"
        table.append(tLine)
    elif classVal2 == classVal3 and classVal2 != classVal1:
        if classVal2 == classificationType.index(testDS[v][2]):
            labelX = ""
        else:
            labelX = " XXX"
        confidence = int((values1[classVal2]+values2[classVal2]+values3[classVal2])/3*100)
        if confidence < confThreshold:
            labelX = labelX + " LOW CONFIDENCE"
        tLine = v+1, testDS[v][2], classificationType[classVal2], labelX, confidence, values1[classVal1], values2[classVal2], values3[classVal3], " - 2,3"
        table.append(tLine)
    else:
        confidence = 0
        tLine = v+1, testDS[v][2],  "Unclassified", "!!!Unclassified!!!", confidence, str(classificationType[classVal1]) + '-' + str(values1[classVal1]), str(classificationType[classVal2]) + '-' + str(values2[classVal2]), str(classificationType[classVal3]) + '-' + str(values3[classVal3]), " - Nill"
        table.append(tLine)
# classificationType = ['Food', 'Cash', 'Monthly Payment', 'Travel', 'Leisure', 'Miscellaneous']
print tabulate(table, headers, tablefmt="simple")
print; print

saveRq = raw_input("Save network node weights? (Y/n) ")
if saveRq == "Y" or saveRq == "y" or saveRq == '':
    from pybrain.tools.customxml.networkwriter import NetworkWriter
    NetworkWriter.writeToFile(net1, 'Aggnet1.xml')
    NetworkWriter.writeToFile(net2, 'Aggnet2.xml')
    NetworkWriter.writeToFile(net3, 'Aggnet3.xml')
    print "Network node weights saved."

print "Done!"

    

