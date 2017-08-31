from lib.util import Util
from bs4 import BeautifulSoup
import re
import time

#通用变量
totalPagePattern   = re.compile(r'_PAGE_COUNT="(\d+)"')
totalPagePattern1  = re.compile(r'_(\d+)\.shtml')
articleFull = '';
caijiUtil   =  Util(rootPath='D:/www/data',host='http://kaoyan.eol.cn',downloadPath='/files/kaoyan1')

#从网址中获取采集到的数据 ，封装成字典数据返回
def caijiUrl(url):
    if not url:
        return None

    content = caijiUtil.getUrlContent(url)
    if not content:
        return None

    soup    = BeautifulSoup(content, 'html5lib')

    article = soup.select('.TRS_Editor')
    article = article[0] if article else None

    title = str(soup.select('.page_title')[0].text)
    tags = soup.select('.n_left a')
    tag = ''; tags.pop()
    for t in tags:
        tag += str(t.text)+ '|'
    tag = tag[0:-1]
    row = {}
    row['title'] = title
    row['tag'] = tag
    row['url'] = url
    row['source_id']='eol'

    #print(tag)
    #文章内容为doc
    if article:
        aNode = article.find('a')
        if aNode:
            href = aNode.attrs['href']
            if href.endswith(".doc"):
                print('下载类型doc')
                href = caijiUtil.buildUrl(href)
                newHref = caijiUtil.download(href)
                aNode.attrs['href'] = newHref
                content = str(aNode)
                row['content'] = content
                row['contentType']='word'
                return row

    # 文章内容为
    articleFull = str(article) if article else ''
    if articleFull:
        # 获取总得页码
        print('下载类型article')
        pageContent = soup.select('#pagenav')
        pageStr = str(pageContent[0]) if pageContent else ''
        pageTotal = caijiUtil.getTotalPage(pageStr)
        #print("共%s页" % (pageTotal))
        if pageTotal > 1:
            for i in range(1, pageTotal):
                url = str(url)
                newUrl = url[0:-6]
                newUrl = newUrl + "_" + str(i) + ".shtml"
                article = caijiUtil.getUrlContent(newUrl, '.TRS_Editor')
                if not  article :
                    return None;
                # print(article)
                articleFull = articleFull + article
            pass
        # print(articleFull)

        content = caijiUtil.downloadImgToLocal(articleFull)
        row['content'] = content
        row['contentType'] = 'article'
        return row

    #内容为flash
    embedDom = soup.select('#mcontent embed')
    if embedDom:
        print( '下载类型falsh' )
        embedSrc = embedDom[0]['src'] if embedDom else '';
        #print(embedDom)
        #print(embedSrc)
        embedSrc = caijiUtil.buildUrl(embedSrc)
        newSrc = caijiUtil.download(embedSrc)
        embedDom[0]['src'] = newSrc
        content = str(embedDom[0])
        row['content'] = content
        row['contentType'] = 'flash'
        return row
    return None







