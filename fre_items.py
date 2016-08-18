#coding=utf-8
from tree import createTree

def findPrefixPath(basePat,treeNode):
    #basePat:item名称,treeNode:item在头表中对应链的第一个节点
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            #讲前缀路径和对应出现的次数添加到字典中,注意frozenset的数据是无序的
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def ascendTree(treeNode, prefixPath): #找当前节点到根节点的路径(从下而上顺序),路径按item的名字存放在prefixPath
    if treeNode.parent != None:
        prefixPath.append(treeNode.name)
        ascendTree(treeNode.parent, prefixPath)


# def mineTree(FPtree, headerTable, minSup, preFix, freqItemList):
#     bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]#(sort header table)
#     for basePat in bigL:
#         newFreqSet = preFix.copy()
#         newFreqSet.add(basePat)
#         freqItemList.append(newFreqSet)
#         condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
#         myCondTree, myHead = createTree(condPattBases, minSup)
#         if myHead != None:
#             mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def mineTree(FPtree, headerTable, minSup, preFix, freqItemList):
    print headerTable
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)