#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from time import sleep


# In[2]:


url  ='http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes'


# In[3]:


def get_data():
    try:
        data = requests.get(url).json()
        df = pd.DataFrame.from_records(data['DATA'], columns=data['COLUMNS'])
        df['DATAHORA'].apply(lambda x: pd.datetime.strptime(x, "%m-%d-%Y %H:%M:%S"))
        return df
    except:
        return pd.DataFrame()


# In[4]:


get_data()


# In[5]:


try:
    all_data = pd.read_csv('all_data.csv')
except:
    all_data = pd.DataFrame()


# In[6]:


all_data.tail()


# In[10]:


y=0
while True:
    all_data = all_data.append(get_data(), ignore_index=True)
    all_data = all_data.drop_duplicates(keep='first')
    all_data.to_csv('all_data.csv', index=False)
    print(all_data.shape)
    y += 1
    if y%10 == 0:
        get_ipython().system('git pull')
        get_ipython().system('git add .')
        get_ipython().system('git commit -m "atualizando dados"')
        get_ipython().system('git push')
    sleep(180)


# In[ ]:




