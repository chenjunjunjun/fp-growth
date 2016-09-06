if __name__=='__main__':
    from loadData import loadSimpData
    from loadData import createInitSet
    from tree import createTree
    from fre_items import mineTree

    dataSet=loadSimpData()
    initSet  = createInitSet(dataSet)
    print 'load data complete!!!'

    FPtree,HeaderTab = createTree(initSet,2)
    print 'FP tree were created!!!'

    freqDict={}
    mineTree(FPtree,HeaderTab,2,set([]),freqDict)
    # for item in freqDict:
    #     print item,freqDict[item]
