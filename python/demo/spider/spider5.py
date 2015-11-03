#-*- coding: UTF-8 -*-
'''
Created on 2013-12-5

@author: good-temper
'''

import urllib2
import bs4
import time

def getPage(urlStr):
    '''
                获取页面内容
    '''
    content = urllib2.urlopen(urlStr).read()
    return content

def getNextPageUrl(currPageNum):
    #http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-页码-1-1-72-4137-33.html
    url =  u'http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-'+str(currPageNum+1)+'-1-1-72-4137-33.html'

    #是否有下一页
    content = getPage(url);
    soup = bs4.BeautifulSoup(content)
    list = soup.findAll('span',{'class':'next-disabled'});
    if(len(list) == 0):
        return url
    return ''

def analyzeList():
    pageNum = 0
    list = []
    url = getNextPageUrl(pageNum)
    while url !='':
        soup = bs4.BeautifulSoup(getPage(url))
        pagelist = soup.findAll('div',{'class':'p-name'})
        for elem in pagelist:
            soup1 =  bs4.BeautifulSoup(str(elem))
            list.append(soup1.find('a')['href'])

        pageNum = pageNum+1
        print pageNum
        url = getNextPageUrl(pageNum)
    return list

def analyzeContent(url):

    return ''

def writeToFile(list, path):
    f = open(path, 'a')
    for elem in list:
        f.write(elem+'\n')
    f.close()

if __name__ == '__main__':
    list = analyzeList()
    print '共抓取'+str(len(list))+'条\n'

    writeToFile(list, u'E:\\jd_phone_list.dat');

