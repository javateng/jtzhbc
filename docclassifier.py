#coding:utf-8
import thulac
import codecs
import json

def getcnwords(doc):
    thu = thulac.thulac('-seg_only')
    wordlist  = thu.cut(doc)
    print ' '.join(wordlist)
    wd = dict([(w,1) for w in wordlist if len(w.decode('utf-8'))>1])
    print wd
    return wd

class classifier:
    def __init__(self, getfeatures):
        self.getfeatures=getfeatures
        self.fc={}
        self.cc={}
    def incf(self, feature,cat):
        self.fc.setdefault(feature,{})
        self.fc[feature].setdefault(cat,0)
        self.fc[feature][cat]+=1
    def incc(self, cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0
    #总的文档数
    def totalcount(self):
        return sum(self.cc.values())
    def categories(self):
        return self.cc.keys()

    def train(self, doc, cat):
        items = self.getfeatures(doc)
        for k in items:
            self.incf(k, cat)
        self.incc(cat)

def main():
    cl = classifier(getcnwords)
    cl.train('我爱北京天安门','good')
    cl.train('赶快来淘宝下订单', 'bad')
    print cl.fc
    print cl.cc
    print cl.totalcount()
    print cl.categories()
    print json.dump()
    with codecs.open('test.txt','wb' ,encoding='utf-8') as f:
        f.write( '%s'.encode('utf-8') % cl.fc )


if __name__=='__main__':
    main()






