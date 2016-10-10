#!/usr/bin/env python
#encoding=utf-8

import requests

DOWNLOAD_URL = u'https://movie.douban.com/top250'

def dowload_page(url):
    data = requests.get(url).content
    return data

def main():
    print download_page(DOWNLOAD_URL)

if __name__ == '__main__':
    main()
