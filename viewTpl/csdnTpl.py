#coding=utf-8
from lib.util import Util
from bs4 import BeautifulSoup
import re
import time
from  lib.dispatchUrl import DispatchUrl
from  dal.articleDal import insertArticle

#通用变量
totalPagePattern   = re.compile(r'_PAGE_COUNT="(\d+)"')
totalPagePattern1  = re.compile(r'_(\d+)\.shtml')
articleFull = '';
caijiUtil   =  Util(rootPath='D:/www/data',host='http://blog.csdn.net')

#从网址中获取采集到的数据 ，封装成字典数据返回
def caijiUrl(url):
    if not url:
        return None
    content = caijiUtil.getUrlContent(url)

    if not content:
        return None

    soup    = BeautifulSoup(content, 'html5lib')

    article = soup.select('#article_content')
    if not article:
        return None;
    article = str(article[0])

    title = str(soup.select('.article_title .link_title')[0].text)
    tags = soup.select('.category_r span')
    tag = '';
    for t in tags:
        tag += str(t.text).strip()+ '|'
    tag = tag[0:-1]
    row = {}
    row['title'] = str(title).strip()
    row['tag'] = tag
    row['url'] = url
    row['source_id']='csdn'
    #print(article)
    content = caijiUtil.downloadImgToLocal(article)
    row['content'] = content
    row['contentType'] = 'article'
    return  row


# exit()
#通用变量
dispathcUrl =  DispatchUrl('csdn')
dispathcUrl.downloading2error()

#row =caijiUrl('http://blog.csdn.net//wcyoot/article/details/32959531')
#print(row)
#exit()
# 循环执行任务 ， 从调度url中获取 ，并指定抓取模板
while 1:
    time.sleep(5)
    #url = dispathcUrl.pop()
    url = dispathcUrl.popError()

    print("下载"+url)
    # print(type(url))
    # exit()
    if not url:
        print("没有下载任务");
        time.sleep(60) ;continue

    row = caijiUrl( url)

    if  row:
        insertArticle(row)
        dispathcUrl.finish(url)
    else:
        dispathcUrl.error(url)
        print("获取内容失败："+url)





