# -*- coding: utf-8 -*-

import pandas as pd
import hashlib

d1={
    'q':'0',
    'a':'1',
    'w':'2',
    's':'3',
    'e':'4',
    'd':'5',
    'r':'6',
    'f':'7',
    't':'8',
    'g':'9',
}
def str2num(s):
    ret=[]
    for example in s:
        ret.append(d1[example])
    return ''.join(ret)

def num2md(num):
    md5=hashlib.md5()
    md5.update(('fenceng'+num).encode(encoding='utf-8'))
    return md5.hexdigest() 


#原手机号
tel_df=pd.read_csv(r'./telsource/tel.txt',header=None)
tel_df.rename(columns={0:'tel_str'},inplace=True)
tel_df['tel_num']=list(map(str2num,tel_df['tel_str'].values))
tel_df['tel_md']=list(map(num2md,tel_df['tel_num'].values))


#加密后的手机号
md1_df=pd.read_csv(r'./telsource/telmd1.txt',header=None)
md2_df=pd.read_csv(r'./telsource/telmd2.txt',header=None)
md1_df.rename(columns={0:'tel_md'},inplace=True)
md2_df.rename(columns={0:'tel_md'},inplace=True)
md_df=pd.concat([md1_df,md2_df])
md_df.reset_index(drop=True,inplace=True)
md_df=md_df.reset_index()

#
md_df1=pd.merge(left=md_df,right=tel_df,on='tel_md',how='left')
#md_df1.iloc[:100000,:].to_excel(r'./telsource/telpick.xlsx',index=False)
md_df1.iloc[100000:150000,:].to_excel(r'./telsource/telpick1.xlsx',index=False)
