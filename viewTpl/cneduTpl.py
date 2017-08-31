from lib.util import Util
from bs4 import BeautifulSoup
import re ,time
from dal.articleDal import insertArticle
from lib.dispatchUrl import DispatchUrl


#通用变量
totalPagePattern   = re.compile(r'_PAGE_COUNT="(\d+)"')
totalPagePattern1  = re.compile(r'_(\d+)\.shtml')
articleFull = '';
caijiUtil   =  Util(rootPath='D:/www/data',host='http://www.cnedu.cn',downloadPath='/files/kaoyan0')

#从网址中获取采集到的数据 ，封装成字典数据返回
def caijiUrl(url):
    if not url:
        return None

    content = caijiUtil.getUrlContent(url)
    if not content:
        return None

    soup    = BeautifulSoup(content, 'html5lib')
    article = soup.select('#fontzoom')
    article = article[0] if article else None

    title = soup.select('.list-left h1')[0].text
    filters = ['2016','2017','2015','2014','2013','2012','2011','2010']
    flag =False
    for fil in filters:
        if title.find(fil)>=0:
            flag =True
            break;
    if not flag:
        return None;

    tag = '专业课'
    row = {}
    row['title'] = title
    row['tag'] = tag
    row['url'] = url
    row['source_id']='eol'

    #print(tag)
    #文章内容为pdf
    if article:
        aNode = article.select('p a')
        aNode = aNode[1] if aNode and len(aNode)==2  else None
        if aNode:
            href = aNode.attrs['href']
            if href.endswith(".pdf"):
                print('下载类型pdf')
                href = caijiUtil.buildUrl(href)
                newHref = caijiUtil.download(href)
                aNode.attrs['href'] = newHref
                content = str(aNode)
                row['content'] = content
                row['contentType']='pdf'
                return row

    # 文章内容为
    if article:
        # 获取总得页码
        print('下载类型article')
        # print(articleFull)
        articleNodes = article.contents
        articleNodes = articleNodes[0:-8]
        articleFull=''
        for node in articleNodes:
            articleFull+=str(node)

        content = caijiUtil.downloadImgToLocal(articleFull)
        row['content'] = content
        row['contentType'] = 'article'
        return row

    return None

dispathcUrl =  DispatchUrl('cnedu_ky')
dispathcUrl.downloading2error()

# 循环执行任务 ， 从调度url中获取 ，并指定抓取模板
while 1:
    #time.sleep()
    url = dispathcUrl.pop()
    #url = dispathcUrl.popError()
    if not url:    break

    print("下载 "+url)
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
        print("获取内容失败：")

print("over")