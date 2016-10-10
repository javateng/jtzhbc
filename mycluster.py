#coding:utf-8
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
from PIL import Image, ImageDraw

class BIcluster:
    def __init__(self, vec, left=None, right=None,distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id

def pearson(s1,s2):
    s1=s1-s1.mean()
    s2=s2-s2.mean()
    xiefangcha = np.sum(s1*s2)
    licha = np.sqrt(np.sum(np.square(s1)))*np.sqrt(np.sum(np.square(s2)))
    return 1-(xiefangcha/licha)

#速度更快
def pearsonx(dfobj):
    data = dfobj.apply(lambda x: x-x.mean())
    data2 = data.apply(lambda x: np.sqrt(np.sum(np.square(x))))
    n = len(data2)
    dist_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            dist_matrix[i][j] = 1.0-np.sum(data.icol(i)*data.icol(j))/(data2[i]*data2[j])
            dist_matrix[j][i] = dist_matrix[i][j]
    return dist_matrix
#超级快，使用DataFrame.corr() 方法

    
def pearson2(s1,s2):
    sum1 = sum(s1)
    sum2 = sum(s2)
    sum1sq = sum(s1**2)
    sum2sq = sum(s2**2)
    psum = sum(s1*s2)
    num = psum-(sum1*sum2/len(s1))
    den = np.sqrt((sum1sq-(sum1**2)/len(s1))*(sum2sq-(sum2**2)/len(s1)))
    if den ==0 :return 0
    return 1-num/den

def hcluster(dfobj, distance=pearson):
    distances = {}
    curclustid = -1

    clust = [BIcluster(dfobj.ix[:,i].copy(), id=i ) for i in range(len(dfobj.columns))]

    while len(clust)>1:
        lowestpair = (0,1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)]=distance(clust[i].vec, clust[j].vec)
                    
                d = distances[(clust[i].id, clust[j].id)]
                if d<closest:
                    closest = d
                    lowestpair = (i,j)
                    
        mergevec = (clust[lowestpair[0]].vec+clust[lowestpair[1]].vec)/2.0
    
        newclust = BIcluster(mergevec,left=clust[lowestpair[0]], right=clust[lowestpair[1]],distance=closest, id=curclustid)

        curclustid -= 1
        #注意下面的索引是先删后面再删前面
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newclust)

    return clust[0]

def printcluster(clust, n=0):
    for _ in range(n):
        print ' ',
    if clust.id<0:
        print '-'
    else:
        print clust.vec.name
    if clust.left!=None:printcluster(clust.left, n=n+1)
    if clust.right!=None:printcluster(clust.right,n=n+1)

#获取聚类的高度
def getheight(clust):
    if clust.left==None and clust.right==None: return 1

    return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    if clust.left==None and clust.right==None: return 0

    return max(getdepth(clust.left), getdepth(clust.right))+clust.distance

def drawnode(draw,clust,x,y,scaling):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2

        #线的长度
        ll = clust.distance*scaling
        #聚类到其子节点的垂直线
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
        #连接左节点和右节点的水平线
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))
        drawnode(draw, clust.left, x+ll,top+h1/2, scaling)
        drawnode(draw, clust.right,x+ll,bottom-h2/2,scaling)
    else:
        draw.text((x+5,y-7),clust.vec.name, (0,0,0))


def drawdendrogram(clust,jpeg='clusters.jpg'):
    h=getheight(clust)*20
    w=1200
    depth = getdepth(clust)

    scaling=float(w-150)/depth

    img = Image.new('RGB',(w,h),(255,255,0))
    draw = ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    drawnode(draw,clust,10,(h/2),scaling)
    img.save(jpeg,'JPEG')


def kcluster(dfobj,distance=pearson,k=4):
    rd_center = [dfobj.max(1)*np.random.rand(len(dfobj)) for _ in range(k)]
    print rd_center
    clust_arr = [[] for _ in range(k)]
    for i in range(len(dfobj.columns)):
        mindistance= distance(dfobj.icol(i), rd_center[0])
        minidx = 0
        for j in range(1,k):
            d = distance(dfobj.icol(i), rd_center[j])
            if d < mindistance :
                mindistance=d
                minidx=j
        clust_arr[minidx].append(dfobj.icol(i).name)
    return clust_arr



#1,输入每一对点之间的距离Dij。
#2,随机在2维平面生成n个点，点i坐标记为x[i]、y[i]，计算它们两之间的距离，记为dij.
#3,对所有i 和j计算：eij=(dij-Dij) / Dij，每个点用一个二维的值grad[k]来表示它要移动的距离的比例因子(初始为0，0)。在计算出每个eij后，计算 ((x[i] - x[j]) / dij)* eij，然后把它加到grad[i][x]上，同样把((y[i] - y[j]) / dij)* eij加到grad[i][y]上。
#4,AssertionError把所有eij的绝对值相加，为总误差，与前一次的总误差比较(初始化为无穷大)，大于前一次的话就停止。否则把它作为上一次总误差，继续。
#5,对每个点，新的坐标为x[i] - = rate * grad[i][x]  y[i] - = rate*grad[i][y]，其中rate是开始时自己定义的一个常数参数，该参数影响了点的移动速度。重新计算各个dij，回到3

def get_dist_matrix(dfobj, distance=pearson):
    n = len(dfobj.columns)
    dist_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            dist_matrix[i][j] = distance(dfobj.icol(i), dfobj.icol(j))
            dist_matrix[j][i] = dist_matrix[i][j]
    return dist_matrix

def xxx(dfobj, distance=pearson, rate=0.01):
    n = len(dfobj.columns)
    rd_xy = np.random.rand(n,2)
    #实际距离
    #distarr = [[ distance(dfobj.icol(i), dfobj.icol(j)) for j in range(n)] for i in range(n)]
    distarr = get_dist_matrix(dfobj)
    lasterror = None
    for k in range(1000):
        print k
        #随机距离
        rd_xy_dist = [[np.sqrt((rd_xy[i][0]-rd_xy[j][0])**2 + (rd_xy[i][1]-rd_xy[j][1])**2 ) for j in range(n)] for i in range(n)]
        mv_xy = np.zeros((n,2))

        totalerror=0.0
        for i in range(n):
            for j in range(n):
                if i==j: continue
                eij = (rd_xy_dist[i][j]-distarr[i][j])/distarr[i][j]
                mv_xy[i][0] += ((rd_xy[i][0]-rd_xy[j][0])/rd_xy_dist[i][j])*eij
                mv_xy[i][1] += ((rd_xy[i][1]-rd_xy[j][1])/rd_xy_dist[i][j])*eij
                totalerror += abs(eij)
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror
        for i in range(n):
            rd_xy[i][0]-= rate * mv_xy[i][0]
            rd_xy[i][1]-= rate * mv_xy[i][1]

    return rd_xy

def draw2d(data, labels, jpeg='mds2d.jpg'):
    img = Image.new('RGB',(2000,2000),(255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    img.save(jpeg,'JPEG')














