#coding=utf-8
import time
from bs4 import BeautifulSoup
from lib.dispatchUrl import DispatchUrl
from lib.util import  Util

dispatchUrl = DispatchUrl()
caijiUtil = Util(host='http://zhenti.kaoyan.eol.cn/')
beginUrls  =[
           'http://kaoyan.eol.cn/shiti/zhengzhi/index.shtml',
           'http://kaoyan.eol.cn/shiti/yingyu/index.shtml',
           'http://kaoyan.eol.cn/shiti/shuxue/index.shtml',
         ]
# 获取所有的的列表页
pageList = []
# 所有的url集合
urlList = []
index = 0
for beginUrl in beginUrls:

    html = caijiUtil.getUrlContent(beginUrl)
    if not html:
        print("获取首页列表失败:: "+beginUrl)
        continue

    soup = BeautifulSoup(html,"html5lib")
    pageList_ = soup.select('.page_left #pagenav')
    totoal = caijiUtil.getTotalPage(str(pageList_[0]))

    #获取所有列表页
    pageList.append(beginUrl)
    for i in range(1,totoal):
        url_ = beginUrl.replace('.shtml','_%s.shtml'%(i))
        pageList.append(url_)

    #获取每个列表页的文章地址
    for page in pageList:
        #提取每个列表页中的地址
        time.sleep(5)
        print("采集列表页中地址："+page)
        html = caijiUtil.getUrlContent(page)
        soup = BeautifulSoup(html,"html5lib")
        tempList = soup.select('.page_left li a')
        for item in tempList:
            href = item.attrs['href']
            if href.startswith('../'):
                continue
            href = caijiUtil.buildUrl(href)
            if href.find('shiti')<0:
                continue
            #urlList.append(href)
            index += 1
            print( "[%s] %s"%(index,href) )
            dispatchUrl.addNewUrl(href)
    pageList = []
print("over")
