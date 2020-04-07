# -*- coding: utf-8 -*-
import random
import time
from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent

# from selenium.webdriver.chrome.options import Options


# 用webdriver获取一个请求头
def get_baidu_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': get_baidu_cookie(),
        'Host': 'www.baidu.com',
        'Referer': 'https://www.baidu.com/',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': str(UserAgent().random)
        }
    return headers


def random_char():
    return ''.join(random.sample('234738-5743189-3485346734-7314-873418', random.randint(5, 10)))


def get_baidu_cookie():
    
    options=webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')    
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_experimental_option('useAutomationExtension',False)      
    
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("http://www.baidu.com")
    time.sleep(1)
    driver.find_element_by_id('kw').send_keys(random_char())
    time.sleep(1)
    driver.find_element_by_id('su').click()
    time.sleep(1)
    c = driver.get_cookies()

    cookies = {}
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    new_cookies = ''
    for item in cookies.keys():
        new_c = '{}={};'.format(item, cookies.get(item))
        new_cookies = new_cookies + new_c
    time.sleep(1)
    #    print(driver.page_source)
    #    url = driver.current_url
    driver.quit()
    return new_cookies


