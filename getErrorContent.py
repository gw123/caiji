from lib.util import Util
from bs4 import BeautifulSoup
import re
from  dal.articleDal import insertArticle
from  lib.dispatchUrl import DispatchUrl
from  viewTpl import eolTpl

import time

#
caijiUtil   =  Util(rootPath='D:/www/data',host='http://kaoyan.eol.cn')
dispathcUrl =  DispatchUrl()

# 循环执行任务 ， 从调度url中获取 ，并指定抓取模板
while 1:
    time.sleep(2)
    url = dispathcUrl.popError()
    exit();
    if not url:
        print("没有下载任务");time.sleep(60) ;continue
    url = str(url.decode('utf-8'))

    row = eolTpl.caijiUrl(url)

    if  row:
        insertArticle(row)
        dispathcUrl.finish(url)
    else:
        dispathcUrl.error(url)
        print("获取内容失败："+url)







