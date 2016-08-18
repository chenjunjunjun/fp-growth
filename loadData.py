#conding=utf-8
def loadSimpData():
    simpDat = [['a','b','e'],
               ['b','d'],
               ['b','c'],
               ['a', 'b', 'd'],
               ['a', 'c'],
               ['b', 'c'],
               ['a','c'],
               ['a','b','c','e'],
               ['a','b','c']]
    return simpDat

def createInitSet():
    dataSet=loadSimpData()
    retDict={}
    for Tid in dataSet:
        retDict[frozenset(Tid)]=1
    return retDict
