from seleniumTest.lib.caiji import Util
from bs4 import BeautifulSoup
import re
from  seleniumTest.kaoyan.dal.articleDal import insertArticle
from  seleniumTest.lib.dispatchUrl import DispatchUrl
from  seleniumTest.kaoyan.viewTpl import eolTpl

import time

#通用变量
totalPagePattern   = re.compile(r'_PAGE_COUNT="(\d+)"')
totalPagePattern1  = re.compile(r'_(\d+)\.shtml')
articleFull = '';
caijiUtil   =  Util(rootPath='D:/www/data',host='http://kaoyan.eol.cn')
dispathcUrl =  DispatchUrl()

# 循环执行任务 ， 从调度url中获取 ，并指定抓取模板
urls = [
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478721.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201401/t20140104_1060598.shtml',
    'http://kaoyan.eol.cn/shiti/shuxue/201512/t20151208_1345927.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478679.shtml',
    'http://kaoyan.eol.cn/shiti/shuxue/201605/t20160513_1397647.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478718.shtml',
    'http://kaoyan.eol.cn/shiti/shuxue/201605/t20160513_1397546.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478722.shtml',
    'http://kaoyan.eol.cn/shiti/shuxue/201605/t20160512_1397173.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478678.shtml',
    'http://kaoyan.eol.cn/shiti/zhengzhi/201612/t20161224_1478726.shtml',
    'http://kaoyan.eol.cn/shiti/shuxue/201512/t20151208_1345911.shtml',
]
while 1:
    time.sleep(2)
    url = urls.pop()
    if not url:
        print("没有下载任务");time.sleep(60) ;continue

    row = eolTpl.caijiUrl(url)

    if  row:
        insertArticle(row)
        dispathcUrl.finish(url)
    else:
        dispathcUrl.error(url)
        print("获取内容失败："+url)







