#coding=utf-8
''' 从FP树中抽取频繁项集的三个基本步骤如下:
    1.从FP树中获得条件模式基；
    2.利用条件模式基，构建一个条件FP树；
    3.迭代重复步骤1步骤2，直到树包含一个元素项为止。
'''
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
#         print newFreqSet
#         condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
#         myCondTree, myHead = createTree(condPattBases, minSup)
#         if myHead != None:
#             mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
'''
递归查找频繁项集:
输入:当前数据集生成的FP树和头表,最小支持度,节点前缀(初始化为空),一个存放查找过程中发现的频繁项集的容器(这里选择了字典,作为输出,初始化为空)
1.对headerTable中的每个元素basePat（按计数值由小到大),循环:
    1.1 basePat + preFix是一个频繁项集，记录下来
    1.2 找以basePat为根,求出它的条件模式基（condPattBases）
    1.3 以condPattBases构造条件FP树
    1.4 若条件FP树不为空时，递归
'''

'''
从fp树挖掘频繁项集是从出现频次低的项开始
1.利用头表构建生成该项的条件模式基，构造条件FP树
2.如果1中生成的条件FP-Tree非单路径FP树，则需要继续循环1步骤构造
3.基于这些条件FP树找频繁项集
'''
def mineTree(FPtree, headerTable, minSup, preFix, freqItemDict):
    #minSup:支持度,freqItemDict:频繁项集存放的地方,preFix:该项的前缀,FPtree:构建的FP树,headerTable:FP树对应的头表
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]  #从频次出现低项开始挖掘
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #preFix是basePat的前缀路径，preFix+basePat是一个频繁项集，出现次数等于basePat出现的次数.当basePat为空时，preFix就是一个单路径FP树，它的路径上所有子集
        # 在构造单路径FP树过程中已经生成了
        print newFreqSet
        #记录每个频繁项的支持度计数
        if frozenset(newFreqSet) in freqItemDict:
            freqItemDict[frozenset(newFreqSet)]+=headerTable[basePat][0]
        else:
            freqItemDict[frozenset(newFreqSet)]=headerTable[basePat][0]
        # print newFreqSet,freqItemDict[frozenset(newFreqSet)]

        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])    #求条件模式基
        myCondTree,myHead = createTree(condPattBases, minSup)
        #实际上，它是以头表判断是否到是单路径FP树，头表为空则表示该basePat的前缀路径是条件FP树,否则，以条件模式基继续构造条件FP树,直到条件FP树为空
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemDict) #FP树中的递归有一个特点:没有返回值,需要记录的数据都放在参数中了,上层可以直接拿到数据
