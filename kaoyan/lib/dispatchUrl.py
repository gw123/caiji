import redis
import time

class  DispatchUrl:
    _rlink = None
    _taskName = ''
    _keyAllUrl = ''          #所有的url用来做排重处理
    _keyToDownload = ''      #待下载的url
    _keyDownloading =''      #正在下载的url , 当出现意外将认为所有运行中的下载任务都没有执行成功 需要从新导入到 toDownload 队列
    _keyFinished = ''        #执行完成的url
    _keyError = ''           #下载出错的url
    #为了任务处理的可靠性 ， 在从任务开始执行 到执行完毕或者执行错误 之间需要加上事务。保证逻辑上的严密性。
    def  __init__(self , taskName='kaoyan'):
        self._taskName  = taskName
        self._keyAllUrl = taskName+"_"+'Allurl'
        self._keyError        = taskName+'_'+'KeyError'
        self._keyFinished     = taskName+"_"+'KeyFinished'
        self._keyDownloading  = taskName +"_"+'KeyDownloading'
        self._keyToDownload   = taskName + '_'+'KeyToDownload'
        self._rlink = redis.Redis(host='192.168.30.128', port=6379, password='gao123456')

    #添加一个新url
    def addNewUrl(self ,url):
        #添加到所有的key ，状态为 待下载
        try:
            if not self._rlink.hexists(self._keyAllUrl,url):
                self._rlink.hset(self._keyAllUrl, url, 'urlToDownload')
                self._rlink.lpush(self._keyToDownload , url)
            else:
                print("重复："+url)
        except Exception:
            print('addNewUrl 失败'+url)

    #从队列中取出来一个要下载的url
    def pop(self):
        runTime =time.time()
        url = self._rlink.rpop(self._keyToDownload)
        if url ==None:
            return None;
        self._rlink.hset(self._keyDownloading,url,runTime)
        self._rlink.hset(self._keyAllUrl,url ,'downloading')
        return url

    #下载完成
    def finish(self,url):
        try:
            self._rlink.hdel(self._keyDownloading,url)
            self._rlink.hset(self._keyFinished,url ,'')
            self._rlink.hset(self._keyAllUrl,url,'finished')
        except Exception:
            print("finish Exception")

    #下载出错  执行3次后还失败报告错误
    def error(self ,url,limitTimes = 3):
        eTime = time.time()
        self._rlink.hdel(self._keyDownloading, url)
        #记录执行错误的队列 并且记录执行的次数
        if( self._rlink.hexists(self._keyError ,url)):
            self._rlink.hincrby(self._keyError,url)
        else:
            self._rlink.hset(self._keyError,url,1)

        self._rlink.hset(self._keyAllUrl,url,'error')


    #主要执行中的队列从新拿到 待执行队列去执行  dwonloading 下载中的队列 ， error 错误队列
    def redo(self ,type='downloading'):
        pass

   # 获取正在下载的网址
    def getDownloadingKey(self):
        return self._rlink.hkeys(self._keyDownloading)

    def getFinishKey(self):
        return  self._rlink.hkeys(self._keyFinished)

    # 获取正在下载的网址
    def getErrorKey(self):
        return self._rlink.hkeys(self._keyError)
    #获取所有的错误包括出粗次数
    def getErrorAll(self):
        return self._rlink.hgetall(self._keyError)
    #获取所有的下载地址
    def getUrlAllKey(self):
        return self._rlink.hkeys(self._keyAllUrl)
    #获取指定url 的下载状态
    def getUrlStatus(self,url):
        return  self._rlink.hget(self._keyAllUrl,url)

    #获取所有网址数目
    def getUrlTotal(self):
        return  self._rlink.hlen(self._keyAllUrl)
    # 获取所有正在下载数目
    def getDownloadingTotal(self):
        return  self._rlink.hlen(self._keyDownloading)
    # 获取所有完成数目
    def getFinishTotoal(self):
        return  self._rlink.hlen(self._keyFinished)
    # 获取所有出错数目
    def getErrorTotal(self):
        return  self._rlink.hlen(self._keyError)