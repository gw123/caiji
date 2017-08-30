#coding=utf-8
from  selenium  import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import sys
from bs4 import BeautifulSoup
from lib.dispatchUrl import DispatchUrl
from lib.util import  Util

#profile = webdriver.FirefoxProfile()
#profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.http', '218.108.107.70')
# profile.set_preference('network.proxy.http_port', 909)  # int
#profile.update_preferences()

driver = webdriver.Firefox()

def getCookie(url):
    driver.get(url)
    sys.stdin.readline()
    cookies = driver.get_cookies()
    return  cookies


