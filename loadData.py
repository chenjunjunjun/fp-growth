#conding=utf-8

def loadSimpData():
    simpDat=[]
    fileIn=open('itemsSet.txt')
    for line in fileIn.readlines():
        lineArr=line.strip().split(',')
        simpDat.append(lineArr)
    fileIn.close()

    return simpDat

def createInitSet(dataSet):
    retDict={}
    for Tid in dataSet:
        retDict[frozenset(Tid)]=retDict.get(frozenset(Tid),0)+1
    return retDict
