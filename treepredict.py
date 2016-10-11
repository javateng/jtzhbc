#coding:utf-8
my_data=[['slashdot','USA','yes',18,'None'],        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],        ['kiwitobes','France','yes',19,'Basic']]

def divideset(rows, col, value):
    split_func = None
    if isinstance(value, int) or isinstance(value, float):
        split_func = lambda row : row[col]>=value
    else:
        split_func = lambda row : row[col]==value
    set1 = [row for row in rows if split_func(row)]
    set2 = [row for row in rows if not split_func(row)]
    return (set1, set2)

class decisionnode:
    def __init__(self, col=-1, value=None,results=None, tnode=None, fnode=None):
        self.col=col
        self.value=value
        self.results=results
        self.tnode=tnode
        self.fnode=fnode

def uniquecounts(rows):
    results = {}
    for row in rows:
        #默认最后一列为结果
        r = row[-1]
        #if r not in results: results[r]=0 效果与下面的等价
        results.setdefault(r,0)
        results[r]+=1
    return results
#基尼不纯度计算
def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp=0
    for k1 in counts :
        p1 = float(counts[k1])/total
        for k2 in counts:
            if k1==k2:continue
            p2 = float(counts[k2])/total
            imp +=p1*p2
    return imp
#熵计算
def entropy(rows):
    from math import log
    total = len(rows)
    log2 = lambda x : log(x)/log(2)
    results = uniquecounts(rows)
    ent=0.0
    for r in results:
        p = float(results[r])/total
        ent = ent - p*log2(p)
    return ent
def buildtree(rows, scoref= entropy):
    if len(rows)==0 :return decisionnode()
    current_score = scoref(rows)
    #定义一些变量临时记录最佳拆分
    best_gain=0.0
    best_criteria = None
    best_sets=None
    #计算变量数量，便于遍历
    col_count = len(rows[0])-1
    for col in range(0, col_count):
        #枚举列中的所有值，根据这些值遍历拆分
        col_values = {}
        for row in rows:
            col_values[row[col]]=1
        for val in col_values:
            (set1, set2) = divideset(rows, col, val)
            #信息增益
            p = float(len(set1))/len(rows)
            gain = current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,val)
                best_sets=(set1,set2)
    #创建子分支
    if best_gain>0 :
        truebranch = buildtree(best_sets[0])
        falsebranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1], tnode=truebranch, fnode=falsebranch)
    else :
        return decisionnode(results=uniquecounts(rows))

def printtree(tree, indent='\t'):
    if tree.results!=None:
        print str(tree.results)
    else:
        print str(tree.col)+':'+str(tree.value)+'?'
        print indent+'T->'
        printtree(tree.tnode, indent+'\t')
        print indent+'F->'
        printtree(tree.fnode, indent+'\t')
#计算叶子数
def getwidth(tree):
    print 'x'
    if tree.tnode==None and tree.fnode==None: return 1
    return getwidth(tree.tnode)+getwidth(tree.fnode)
def getdepth(tree):
    if tree.tnode==None and tree.fnode==None: return 0
    return max(getdepth(tree.tnode), getdepth(tree.fnode))+1



def main():
    sets = divideset(my_data, 2, 'yes')
    print sets
    print uniquecounts(my_data)
    print '基尼不纯度：', giniimpurity(my_data)
    print '熵：', entropy(my_data)
    tree = buildtree(my_data)
    printtree(tree)
    print '---------------------------------'
    print getwidth(tree)

if __name__ == '__main__':
    main()