import time
from bs4 import BeautifulSoup
from lib.dispatchUrl import DispatchUrl
from lib.util import  Util

dispatchUrl = DispatchUrl()
caijiUtil = Util(host='http://www.cnedu.cn/')
beginUrls  =[
           'http://www.cnedu.cn/examination/courses/page1.shtm',
         ]
# 获取所有的的列表页
pageList = []
# 所有的url集合
urlList = []
index = 0
failLvl2Urls = open('./data/failLvl2Urls.txt','a')
failLvl1Urls = open('./data/failLvl1Urls.txt','a')

for beginUrl in beginUrls:
    html = caijiUtil.getUrlContent(beginUrl)
    if not html:
        print("获取首页列表失败:: "+beginUrl)
        failLvl1Urls.write(beginUrl)
        continue
    #soup = BeautifulSoup(html,"html5lib")
    totoal = 1655;
    #获取所有列表页
    #pageList.append(beginUrl)
    for i in range(796,totoal):
        url_ = beginUrl.replace('1.shtm','%s.shtm'%(i))
        pageList.append(url_)

    #获取每个列表页的文章地址
    for page in pageList:

        #提取每个列表页中的地址
        time.sleep(5)
        print("采集列表页中地址："+page)
        html = caijiUtil.getUrlContent(page)
        if not html:
            print('获取内容失败')
            failLvl2Urls.write(page)
            continue

        soup = BeautifulSoup(html,"html5lib")
        tempList = soup.select('.listbox li a')
        for item in tempList:
            href = item.attrs['href']
            if href.startswith('../'):
                continue
            href = caijiUtil.buildUrl(href)

            #urlList.append(href)
            index += 1
            print( "[%s] %s"%(index,href) )
            dispatchUrl.addNewUrl(href)
    pageList = []
print("over")
