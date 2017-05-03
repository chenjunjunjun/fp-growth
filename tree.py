#coding=utf-8
class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        #节点名称
        self.name=nameValue
        #节点在该路径总共出现次数
        self.count=numOccur
        #nodeLink:下一个同名节点的地址,构成整个头表的链,方便对FP树的快速访问
        self.nodeLink=None
        #节点的前一个节点(父节点)
        self.parent=parentNode
        #节点的孩子节点,因为孩子节点的个数不确定,并非什么二叉树,所以用一个字典存放,key:子节点的名称,value:子节点的地址
        self.children={}

    def inc(self,numOccur):
        self.count+=numOccur



def createTree(dataSet,minSup=2):
    # 首先我们思考一下创建FP树的过程

    '''
    一般我们分两步：
    第一步:先扫描一遍数据集,过滤掉非频繁项，得到频繁1项集,同时需要存储它们出现的次数,因为第二遍扫描记录时，需要根据
    第二步:再一次扫描数据集，对每一条记录，去掉非频繁项，然后对记录中的项按出现次数从高到底排序，然后插入FP树
    '''

    # 第一步
    headerTable={}
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

    '''
    头指针表:FP-growth算法还需要头表，存储每个节点链的第一个节点地址，每个节点通过nodeLink指向下一个节点，
    这样就构成一个单链表
    '''
    # 初始化头表
    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    #到这里,头表节点的数据结构为:item:[item出现次数,FP树中该元素的第一个节点地址],初始化为空,创建树的时候会进行赋值，这就实现了头表的功能.
    #这里通过字典的value值是一个列表，列表的第一个值相当于链表的值，第二值相当于指向下一个节点的指针，这种方法很巧妙
    # 是不是C种的链表在python种可以通过字典来模拟实现呢？
    # print headerTable

    # 第二步
    #其实就是将一条记录中满足支持度的商品筛选出来,排序后,按顺序插入到一个树中,并更新头表
    root=treeNode('Null Set',0,None)
    #第二次扫描数据集，对每一条记录先过滤掉非频繁项，后排序，再插入到FP树
    dataSet_tuple=dataSet.items()
    for tranSet,count in dataSet_tuple:
        #tranSet是一条记录,用得是frozenset存储
        localD={}
        for item in tranSet:
            if item in freqItemSet:
                localD[item]=headerTable[item][0]
        #localD中存放是tranSet中大于minSup元素的key和在dataSet中出现的次数,是一个key-value
        if len(localD)>0:
            #将localD按照item出现次数从高到低排序,并存储在orderedItems中
            orderedItems = [v[0] for v in sorted(localD.items(),key = lambda p:p[1],reverse = True)]
            # 插入到FP树中,每一条记录都是从根节点插入
            insert_treeNode(orderedItems,root,headerTable,count)
    return root,headerTable


'''构建fp树分两步:
1.插入树节点
2.更新头表
'''
def insert_treeNode(items, into_treeNode, headerTable, count):
    #items:待插入的节点序列(已经排好序),into_treeNode:插入节点的位置(其实是插入到该节点的children),headerTable:因为插入时需要更新头节点,所以传入

    #每次插入的是items的第一个item,它出现的频率最高，接下来插入的是第二高的,依次类推
    if items[0] in into_treeNode.children:
        into_treeNode.children[items[0]].inc(count)
    else:
        into_treeNode.children[items[0]] = treeNode(items[0], count, into_treeNode) #初始化要插入节点,并插入到当前节点

        #更新头表,headerTable的value值第二项是记录每个节点子节点地址
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = into_treeNode.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], into_treeNode.children[items[0]]) #headerTable[items[0]][1]其实是一个树节点

    if len(items) > 1: #插入序列中剩下的item，这里用递归非常方便，也好理解
        insert_treeNode(items[1:], into_treeNode.children[items[0]], headerTable, count) #此时插入的的位置从into_treeNode.children[items[0]]开始了

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

