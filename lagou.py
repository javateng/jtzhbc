#!/usr/bin/env python
#encoding=utf-8

import requests
from bs4 import BeautifulSoup as bsp

DOWNLOAD_URL = u'http://www.lagou.com/zhaopin/Python/?labelWords=label'

def download_page(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    data = requests.get(url,headers = headers).content
    return data

movie_name_list=[]

def parse_html(html):
    soup = bsp(html)
    position_soup = soup.find('ul',class_='item_con_list')

    for position_li in position_soup.find_all('li'):
        position_attr = position_li.attrs
        print position_attr.get('data-salary')
        print position_attr.get('data-company')
        #detail = movie_li.find('div',class_='hd')
        #movie_name=detail.find('span',class_='title').getText()
        #movie_name_list.append(movie_name)

    #next_page = soup.find('span', class_='next').find('a')
    #if next_page:
     #   return movie_name_list, DOWNLOAD_URL+next_page['href']
    #return movie_name_list, None

def main():
    #print download_page(DOWNLOAD_URL)

    url = DOWNLOAD_URL
    html = download_page(url)
    parse_html(html)
    #while url :
     #   html=download_page(url)
     #   movies, url = parse_html(html)
    #print '\n'.join(movies)

if __name__ == '__main__':
    main()
