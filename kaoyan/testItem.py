from seleniumTest.lib.caiji import Util
from bs4 import BeautifulSoup
import re
from  seleniumTest.kaoyan.item import insert
from  seleniumTest.lib.dispatchUrl import DispatchUrl
import time
#通用变量
totalPagePattern   = re.compile(r'_PAGE_COUNT="(\d+)"')
totalPagePattern1  = re.compile(r'_(\d+)\.shtml')
articleFull = '';
caijiUtil   =  Util(rootPath='D:/www/data',host='http://kaoyan.eol.cn')
dispathcUrl =  DispatchUrl()

content = caijiUtil.getUrlContent('http://kaoyan.eol.cn/shiti/shuxue/201708/t20170801_1545073.shtml')

soup = BeautifulSoup(content ,'html5lib')

article = soup.select('.TRS_Editor')[0]

docNode = article.find('a')
if docNode:
    href = docNode.attrs['href']
    if href.endswith(".doc"):
        href = caijiUtil.buildUrl(href)
        print(href)
    else:
        print('nt')




