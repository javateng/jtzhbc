#coding:utf-8
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

df = DataFrame(critics)
#正确版本
def sim_distance(dfobj, p1, p2):
    dfobj2 = dfobj[[p1,p2]].dropna()
    if len(dfobj2)==0:
        return 0
    
    return 1/(1+np.sqrt(((dfobj2[p1]-dfobj2[p2])**2).sum()))

#书中用的是这个版本
def sim_distance2(dfobj, p1, p2):
    dfobj2 = dfobj[[p1,p2]].dropna()
    if len(dfobj2)==0:
        return 0
    
    return 1/(1+((dfobj2[p1]-dfobj2[p2])**2).sum())

def sim_pearson(dfobj, p1, p2):
    dfobj2 = dfobj.ix[:,[p1,p2]].dropna()
    if len(dfobj2)==0:
        return 0
    #这里的目的是为了创建一个相同值得数组以方便汇总成一条记录而已
    groupkey=np.array(['a']*len(dfobj2))
    xiefangcha = sum([x*y for x,y in dfobj2.groupby(groupkey).apply(lambda x: x-x.mean()).values])
    licha = np.sqrt(dfobj2.groupby(groupkey).apply(lambda x: (x-x.mean())**2).sum())
    return xiefangcha/(licha[0]*licha[1])
     
def topMatches(dfobj, p,n=5, similarity=sim_pearson):
    score =[(similarity(dfobj,x,p), x) for x in dfobj.columns if x!=p]
    score.sort()
    score.reverse()
    return score[:n]


def getRecommendations(dfobj,people, similarity=sim_pearson):
    dfobj2 = dfobj.drop(people,axis=1)
    cor_df= Series(dict([(p,similarity(dfobj,p,people)) for p in dfobj2]))
    mul_df = DataFrame.mul(dfobj2.T, cor_df[cor_df>0],axis=0)
    return Series.div(mul_df.sum(),DataFrame.mul(pd.notnull(mul_df),cor_df,axis=0).sum()).order(ascending=False)[pd.isnull(dfobj[people])]

def calculateSimilarItems(dfobj,similarity=sim_pearson):
    sim={}
    for obj_x in dfobj.columns:
        sim[obj_x]=topMatches(dfobj,obj_x,n=len(dfobj.columns)-1, similarity=similarity)
    return sim

itemsim = calculateSimilarItems(df.T)
#书中用的是下面这个itemsim结果
itemsim2 = calculateSimilarItems(df.T, similarity=sim_distance2)
def getRecommendedItems(dfobj,itemMatch, user):
    #获取user已购买物品
    buyedItems = dfobj[user].dropna()
    scores={}
    simsum={}
    for item1 in buyedItems.index:
        
        for (simval, item2) in itemMatch[item1]:
            if item2 in buyedItems.index:
                continue
            scores.setdefault(item2,0.)
            scores[item2]+=simval*buyedItems[item1]
            simsum.setdefault(item2,0.)
            simsum[item2]+=simval

    ranking = [(scores[item]/sv , item) for item, sv in simsum.items()]
    ranking.sort()
    ranking.reverse()

    return ranking
    






