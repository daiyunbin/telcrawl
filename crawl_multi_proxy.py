#coding=utf-8
import json
import requests
from bs4 import BeautifulSoup
#请求地址
targetUrl = "https://www.baidu.com/s?wd=13127965029&tn=json"

#代理服务器
proxyHost = '121.46.234.76'
proxyPort = "717"

proxyMeta = "http://%(host)s:%(port)s" % {

    "host" : proxyHost,
    "port" : proxyPort,
}

proxies = {

    "http"  : proxyMeta,
}

resp = requests.get(targetUrl,headers=headers,proxies=proxies)
print(resp.text)


url=r'http://ip.chinaz.com/'
proxy={'http': 'http://58.218.214.136:16749',
       'https': 'https://58.218.214.136:16749'}
res=requests.get(targetUrl,headers=headers)
json.loads(res.text)


html=BeautifulSoup(res.text,'lxml')
nr=html.select('.fz24')[0].text
print(nr)