from lib.util import Util
from bs4 import BeautifulSoup
import re
from  dal.articleDal import insertArticle
from  lib.dispatchUrl import DispatchUrl
from  viewTpl import eolTpl
from  viewTpl import cneduTpl
import time

#通用变量
dispathcUrl =  DispatchUrl()

# 循环执行任务 ， 从调度url中获取 ，并指定抓取模板
while 1:
    time.sleep(5)
    url = dispathcUrl.pop()
    if not url:
        print("没有下载任务");time.sleep(60) ;continue

    if url.find('http://www.cnedu.cn/')>=0:
        print('采集：'+url)
        row = cneduTpl.caijiUrl(url)
    else:
        row = eolTpl.caijiUrl(url)

    if  row:
        insertArticle(row)
        dispathcUrl.finish(url)
    else:
        dispathcUrl.error(url)
        print("获取内容失败："+url)







