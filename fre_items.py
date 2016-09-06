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
    1.1 记basePat + preFix为当前频繁项集newFreqSet,它也是查找树过程中发现的一个频繁项集
    1.2 将newFreqSet添加到freqItemList中
    1.3 找以basePat为根,查它的前缀路径;计算t的条件FP树（myCondTree、myHead）
    1.4 当条件FP树不为空时，继续下一步；否则退出递归
    1.4 以myCondTree、myHead为新的输入，以newFreqSet为新的preFix，外加freqItemList，递归这个过程
'''


def mineTree(FPtree, headerTable, minSup, preFix, freqItemDict):
    #minSup:支持度,freqItemList:频繁项集存放的地方,preFix:请传入一个空集合(set([])),在函数中用于保存当前前缀,FPtree:构建的FP树,headerTable:FP树对应的头表
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #basePat+preFix为以basePat为根节点的一个频繁项集.至于preFix(单链)子集+basePat是频繁项集,这是人为我们知道,而且计算机并没有函数计算一个集合的子集,
        # 实际是通过递归来求出他们的子集,这个程序的代码很好的说明了思路,这个思路在网上博客上面的例子讲得非常清晰
        print newFreqSet
        #记录每个频繁项的支持度计数
        if frozenset(newFreqSet) in freqItemDict:
            freqItemDict[frozenset(newFreqSet)]+=headerTable[basePat][0]
        else:
            freqItemDict[frozenset(newFreqSet)]=headerTable[basePat][0]
        # print newFreqSet,freqItemDict[frozenset(newFreqSet)]

        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree,myHead = createTree(condPattBases, minSup)
        #找该basePat的前缀路径,然后构建条件FP树,直到条件FP树为空
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemDict) #FP树中的递归有一个特点:没有返回值,需要记录的数据都放在参数中了,上层可以直接拿到数据
