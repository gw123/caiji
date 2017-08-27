#coding=utf-8
from  selenium  import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import time
from bs4 import BeautifulSoup
from seleniumTest.lib.dispatchUrl import DispatchUrl
from seleniumTest.lib.caiji import  Util
import redis
#profile = webdriver.FirefoxProfile()
#profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.http', '218.108.107.70')
# profile.set_preference('network.proxy.http_port', 909)  # int
#profile.update_preferences()

driver = webdriver.Firefox()
driver.get('http://zhenti.kaoyan.eol.cn/')

dispatchUrl = DispatchUrl()

tempLinks = driver.find_elements_by_css_selector('td a')
#提取要下载的链接
for link in tempLinks:
    text = link.text
    if(text=='试卷' or text=='答案'):
        href = link.get_attribute('href')
        if ( href!=''):
            dispatchUrl.addNewUrl(href)
    pass

cookies = driver.get_cookies()
#res = dispatchUrl.getUrlAllKey()
#print(res)
#driver.find_element_by_css_selector('div.btn:nth-child(1) > span:nth-child(1)').click()

