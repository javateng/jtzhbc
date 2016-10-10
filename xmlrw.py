#coding:utf-8
from bs4 import BeautifulSoup as bsp

f = open('python_search.xml')
soup = bsp(f.read())
print soup.prettify()