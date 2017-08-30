#coding=utf-8
from  selenium  import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import time
from bs4 import BeautifulSoup
from lib.dispatchUrl import DispatchUrl
from lib.util import  Util
import redis,re
#profile = webdriver.FirefoxProfile()
#profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.http', '218.108.107.70')
# profile.set_preference('network.proxy.http_port', 909)  # int
#profile.update_preferences()
dispatchUrl = DispatchUrl('csdn')
caijiUtil   = Util(host='http://blog.csdn.net/')

#博主列表的第一页
beginUrls = [  'http://blog.csdn.net/wcyoot/article/list/1',]

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
    pageList_ = soup.select('#papelist a')
    #print(pageList_[-1])
    #exit()
    if pageList_:
        totalPagePattern = re.compile(r'(\d+)$')
        pageTotal_ = totalPagePattern.search(pageList_[-1].attrs['href'])
        if pageTotal_:
            totoal = int(pageTotal_.group(1))
        else:
            totoal =1
    else:
        totoal =1

    #获取所有列表页
    pageList.append(beginUrl)
    for i in range(1,totoal):
        beginUrl_=beginUrl[0:beginUrl.rfind('/')]
        url_ = beginUrl_+"/"+str(i)
        pageList.append(url_)

    #获取每个列表页的文章地址
    for page in pageList:
        #提取每个列表页中的地址
        time.sleep(5)
        print("采集列表页中地址："+page)
        html = caijiUtil.getUrlContent(page)
        if not  html:
            print("获取内容失败")
            continue
        soup = BeautifulSoup(html,"html5lib")
        tempList = soup.select('.list_item_new .link_title a')
        if not tempList:
            print("获取 link_title a内容失败")
            continue

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
