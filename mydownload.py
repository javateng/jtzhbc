#coding:utf-8
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def tanimoto(s1,s2):
    cnt1 = s1.sum()
    cnt2 = s2.sum()
    shr = (s1&s2).sum()
    return 1.0-(float(shr)/(cnt1+cnt2-shr))

def test(dfobj):
    
    return [[tanimoto(dfobj.icol(i), dfobj.icol(j)) for j in range(len(dfobj.columns))] for i in range(len(dfobj.columns))]
