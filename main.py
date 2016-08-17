if __name__=='__main__':
    from tree import createTree
    from loadData import createInitSet

    initSet  = createInitSet()
    FPtree,HeaderTab = createTree(initSet,3)
    a = FPtree.disp()
