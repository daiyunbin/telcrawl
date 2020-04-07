# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 09:54:11 2020
批量爬取100w的数据
@author: jie
"""

import warnings
warnings.filterwarnings('ignore')

import time
import random
import os
import re
import json
import pandas as pd


import requests
import threading
from queue import Queue


from whitelist import white_list,white_list1
from headers import get_baidu_headers


class QiubaiSpider:
    def __init__(self):
        self.url_temp = "https://www.baidu.com/s?wd={}&tn=json"
        self.filepath=r'./tel100w/mobile.xlsx'
        self.savepath=''
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}       
        self.white_list=white_list        
        self.white_list1=white_list1
        self.step=1
        self.url_queue = Queue()
        self.json_queue = Queue()
        self.content_queue = Queue()
        self.start=0
    
    def get_url_list(self):
        df=pd.read_excel(self.filepath)
        data=df.values[self.start:self.start+self.step]
        for i in range(len(data)):
            self.url_queue.put(self.url_temp.format(data[i][0]))
 
    def parse_url(self):
        while True:
            url = self.url_queue.get()
            #print(self.headers)
            response = requests.get(url,headers=self.headers)
            try:
                ret = json.loads(response.text)
                data=ret['feed']['entry']  
            except:
                print('出现异常')
                data=[]
            content_list = []
            for every_data in data:
                if every_data:
                    item = {}
                    tel=every_data['category']['value']
                    title=every_data['title']
                    content=every_data['abs']
                    sub_url=every_data['url']
                    
                    sub_url=re.sub('^https?://','',sub_url)
                    if sub_url.split('.')[1]=='izhufu' or sub_url.split('.')[1]=='jihaoba' or sub_url.split('.')[1]=='xysjk':
                        pass
                    else:
                        if sub_url.split('.')[0] in white_list:
                            domain=sub_url.split('.')[1]
                        else:
                            domain=sub_url.split('.')[0]            
                        if domain not in white_list1  and '查號' not in title and '查号' not in title and '归属地' not in title and '号段' not in title and '靓号' not in title:              
                            item["telno"] = tel
                            item["title"]=title
                            item["content"]=content
                            item["sub_url"]=sub_url 
                            content_list.append(item)                  
            self.content_queue.put(content_list)
            self.url_queue.task_done()
 
    def save_content_list(self): # 保存
        #all_tel=[]    
        while True:
            content_list = self.content_queue.get()
            with open(self.savepath, "a", encoding="utf-8") as f:
                for content in content_list:
                    if content:
#                        all_tel.append(content)
                        json.dump(content,f,ensure_ascii=False,indent=4)
                        f.write('\n') 
#            ret=[info['telno'] for info in all_tel]
#            print('100个查询到{}个'.format(len(set(ret))))            
            self.content_queue.task_done()

  
    def run(self): # 实现主要逻辑
        thread_list = []
        #1.url_list
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)
        #2.遍历，发送请求，获取响应,取数
        for i in range(25):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        #3.保存
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)
 
        for t in thread_list:
            t.setDaemon(True) # 把子线程设置为守护线程，该线程不重要 主线程结束，子线程结束
            t.start()
 
        #
        for q in [self.url_queue,self.content_queue]:
            q.join() # 让主线程等待阻塞，等待对列的任务完成之后再完成
 
        #print("主线程结束")
    
    
#选取前num到num+10000的手机号码，总共测10000个。每次并行搜索100个，
def save(num):
    QS=QiubaiSpider()
    savepath_index=1
    start=time.time()
    main_path=r'./output100w/savefile{}'.format(num)
    #创建文件夹
    if not os.path.exists(main_path):
        os.makedirs(main_path)    
    for index in range(num+2000*1,num+10000,100):      ###改  
        QS.start=index 
        QS.step=100
        if (index-num)%2000==0:
            QS.savepath=r'./output100w/savefile{}/request{}.json'.format(num,savepath_index+1)  ###改 
            print(QS.savepath)
            savepath_index+=1
        if (index-num)%1000==0:
            QS.headers=get_baidu_headers()
        time.sleep(random.uniform(2,4))
        QS.run()
        print('index:',index,'用时:',time.time()-start)
        time.sleep(random.uniform(40,60)) 
        
#
if __name__=='__main__':
    save(0)        
#        


def json2excel(path,df):
    with open(path,'r',encoding="utf-8") as f:
        all_text=f.read()
    all_text_list=all_text.split('\n')   
    
    #上面得到的list按顺序变成[[...],[...]....],即每个号码变成一个子list    
    all_text_split=[]
    for i in range(0,len(all_text_list),6):
        b=all_text_list[i:i+6]
        all_text_split.append(b)  
        
    #[{},{},{}...],每个号码变成一个字典
    list_dic=[]
    for example in all_text_split[:-1]:
        string=''
        for sub in example:
            string+=sub
        list_dic.append(json.loads(string))

    ret=[]
    l1=[]
    for example in list_dic:
        if example['telno'] not in ret:
            ret.append(example['telno'])
            l1.append(df[df['tel']==int(example['telno'])].iloc[0,0])
    return len(ret),l1.sort()
