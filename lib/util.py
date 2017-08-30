#coding=utf-8
#数据处理工具集和
import re ,random ,time ,os
from  urllib import  request
from  datetime  import date
from bs4 import BeautifulSoup
import hashlib

import imghdr
# 可以传 str（） 字节数据 但是两者的解析有区
#使用selenium
def switch_window_by_part_title(part ,driver):
  windowHandles = driver.window_handles
  for  win in windowHandles:
    driver.switch_to_window(win)
    title = driver.title
    if(title.find(part)>=0):
      return

def switch_to_last_window(driver):
    windowHandles = driver.window_handles
    win =windowHandles[-1]
    driver.switch_to_window(win)

class  Util:
    rootPath     = 'D:/www/data' #网站根路径
    downloadPath = '/files/temp' #相对网站路径

    host = ''#抓取网站的域名
    imgTagSrcPattern  = '';
    hostParttern = '';
    currentUrlpath = '' #当前抓取的地址所在路径

    headers = {
	'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
	'Referer':'http://blog.csdn.net'
	}
    def __init__( self,  host='' , rootPath=''):
        self.rootPath = rootPath
        self.host = host
        self.imgTagSrcPattern = re.compile(r'src="(.*?)"')
        self.hostParttern = re.compile(r'^[\w\.]*?\.\w{1,5}\/\w*')

    #获取url 的内容
    def getUrlContent(self,url,selector=''):

        self.currentUrlpath = url[0:url.rfind('/')]
        newRequest = request.Request(url);
        for i in self.headers:
            newRequest.add_header(i, self.headers[i])
        html = ''

        try:
            netFile = request.urlopen(url=url,timeout=10)
            html = netFile.read()
        except Exception:
            print("Exception 获取内容失败:"+url)
            return None
        if selector:
            soup = BeautifulSoup(html, 'html5lib')
            content = soup.select(selector)

            return str(content[0]) if content else '';
        else:
            return html

    #从指定为url中下载文件 ,加一个md5防止文件重复下载
    #webRoot 站点文件根目录
    def download(self,url ):

        newRequest =request.Request(url);
        for i in self.headers:
          newRequest.add_header( i , self.headers[i] )
        try:
            netFile = request.urlopen(newRequest ,timeout =20)
            imageContent = netFile.read()
        except Exception :
            print("网页异常："+url)
            return url

        md5obj = hashlib.md5()
        md5obj.update(imageContent)
        hash = md5obj.hexdigest()
        md5obj.update(('_xytschool'+hash).encode('utf-8'))
        hash = md5obj.hexdigest()

        filePath ,webPath = self.makePath(url,hash)
        #判断文件是否存在
        if os.path.isfile(filePath):
            return webPath;

        file = open( filePath , 'wb+' )
        file.write(imageContent)
        return  webPath;

    #创建一个随机文件
    def makeRandPath(self ,url):
        ext = url.split('.')[-1]
        dateStr = date.today()
        #dateStr = dateStr.split('-').join('');
        path = "%s/%s/"%(self.rootPath ,dateStr)
        if os.path.exists(path)==False:
          os.makedirs(path)
        tt = time.time();
        rand=random.randint(1000,9999)
        return  "%s/%d%d.%s"%(path,tt,rand,ext)

    #filePath 下载到本地的地址 ， webPath图片网址
    def makePath(self , url,hashStr):
        #print( url)
        ext = url.split('.')[-1]

        if ext not in ['png','jpg','jpeg','gif']:
            ext ='png'
        path = "%s/%s/xyt%s"%(self.rootPath,self.downloadPath ,hashStr[11:15])
        webPath = "%s/xyt%s/school%s.%s" % ( self.downloadPath, hashStr[11:15], hashStr, ext)
        filePath = "%s/%s/xyt%s/school%s.%s" % (self.rootPath, self.downloadPath, hashStr[11:15], hashStr, ext)
        filePath = filePath.replace('//','/')
        #print("路径 :%s"%(path))
        if os.path.exists(path)==False:
          os.makedirs(path)
        return  filePath,webPath

    #获取文件的完整下载文件的路径
    def buildUrl(self,url):
     #print("old:"+url)
     url = url.replace(' ' ,'%20')
     if url.startswith('http'):
         return url
     else:
        match = self.hostParttern.search(url)
        if match:
            if ( url.startswith('//') ):
                url= 'http:'+url
            else:
                url= 'http://'+url
        elif  url.startswith('/'):
             url=self.host+url
        else:
             url=url.replace('./','')
             url = self.currentUrlpath+ "/" +url
     #print("after:"+url)
     return url

    #将文章中的图片下载到本地 content 页面内容  ,seletor 文章所在的element元素
    #返回替换图片后的文章内容
    def downloadImgToLocal(self ,content ):

        soup = BeautifulSoup(content, "html5lib")
        #解析文档内容
        #找到所有的图片
        tag_imgs = soup.select('img')
        if not  tag_imgs:
            return content
        for img in tag_imgs:
            #print(img.attrs)
            src = img.attrs['src']
            src = self.buildUrl(src)
            #print('下载图片=>:',src)
            newPath = self.download(src)
            img['src'] = newPath
            #print('下载完成 <>: ' + newPath)
        str1 = str(soup.body)
        str1 = str1.replace("<body>",'')
        str1 = str1.replace("</body>",'')
        return  str1

    #从获取分页总数目
    def getTotalPage(self ,content):
        totalPagePattern = re.compile(r'_PAGE_COUNT="(\d+)"')
        pageTotal_ = totalPagePattern.search(content)
        if pageTotal_:
            pageTotal = int(pageTotal_.group(1))
            return  pageTotal

        totalPagePattern1 = re.compile(r'_(\d+)\.shtml')
        soup = BeautifulSoup(content, 'html5lib')
        # 获取总得页码
        pageBtns = soup.select('.pl')

        # 解析获取总得页码
        if pageBtns:
            lastPageBtn = pageBtns[-1]
            href = lastPageBtn.attrs['href']
            pageTotal_ = totalPagePattern1.search(href)
            if pageTotal_:
                pageTotal = int(pageTotal_.group(1))
                return  pageTotal

        return 1;

# util = Util('D:/www/data' , 'http://c.csdnimg.cn')
# url = util.buildUrl(url)
# filePath= util.download(url)
