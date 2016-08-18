if __name__=='__main__':
    from tree import createTree
    from loadData import createInitSet
    from fre_items import mineTree

    initSet  = createInitSet()
    FPtree,HeaderTab = createTree(initSet,2)
    freqList=[]
    mineTree(FPtree,HeaderTab,2,set([]),freqList)
    b=len(freqList)
    # print b
    # for item in freqList:
    #     print item
