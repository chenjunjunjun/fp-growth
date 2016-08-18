#coding=utf-8
class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        #节点名称
        self.name=nameValue
        #节点在该路径出现次数
        self.count=numOccur
        #nodeLink:下一个同名节点的地址,构成整个头表的链,方便对FP树的快速访问
        self.nodeLink=None
        #节点的前一个节点(父节点)
        self.parent=parentNode
        #节点的孩子节点,因为孩子节点的个数不确定,并非什么二叉树,所以用一个字典存放,key:子节点的名称,value:子节点的地址
        self.children={}

    def inc(self,numOccur):
        self.count+=numOccur

    #fp树的展示
    def disp(self,ind=1):
        print ' '*ind,self.name,' ',self.count
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet,minSup=1):
    '''头指针表'''
    headerTable={}
    #dataSet的键是frozenSet,第一次扫描数据集
    for T in dataSet:
        for item in T:
            headerTable[item]=headerTable.get(item,0)+dataSet[T]

    #去掉不满足最小支持度的item
    for k in headerTable.keys():
        if headerTable[k]<minSup:
            del headerTable[k]
    # print headerTable

    freqItemSet=set(headerTable.keys())
    if len(freqItemSet)==0:
        return None,None

    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    #最后,头表节点的数据结构为:item:[item出现次数,下一个节点的地址],看看人家是如何设计的节点,可以借鉴
    retTree=treeNode('Null Set',1,None)

    # print headerTable
    #第二次扫描数据集
    dataSet_tuple=dataSet.items()
    for tranSet,count in dataSet_tuple:
        #tranSet是一条记录,用得是frozenset存储
        localD={}
        for item in tranSet:
            if item in freqItemSet:
                localD[item]=headerTable[item][0]
        #localD中存放是tranSet中大于minSup元素的key和在dataSet中出现的次数,是一个key-value
        if len(localD)>0:
            #将localD按照item出现次数从高到低排序,并存储在列表中
            orderedItems = [v[0] for v in sorted(localD.items(),key = lambda p:p[1],reverse = True)]
            insert_treeNode(orderedItems,retTree,headerTable,count)
            #这里其实是向根节点中插入新节点,但是和二叉树的创建不一样,因为这里插入子节点不返回地址,因为不想二叉树有特定的左指针和右指针
    return retTree,headerTable


def insert_treeNode(items, inTree, headerTable, count):
    #items:要插入的对象,inTree:要插入的节点,headerTable:因为插入时需要更新头节点,所以传入

    #每次插入的是items的第一个item,因为它出现的频率最高
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree) #初始化要插入节点,并插入到当前节点

        #更新头表,headerTable的value值第二项是记录每个节点子节点地址
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    #插入items剩下的item
    if len(items) > 1:
        insert_treeNode(items[1:], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

