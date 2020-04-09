#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import requests
from time import sleep


# In[ ]:


url  ='http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes'


# In[ ]:


def get_data():
    try:
        data = requests.get(url).json()
        df = pd.DataFrame.from_records(data['DATA'], columns=data['COLUMNS'])
        df['DATAHORA'].apply(lambda x: pd.datetime.strptime(x, "%m-%d-%Y %H:%M:%S"))
        return df
    except:
        return pd.DataFrame()


# In[ ]:


get_data()


# In[ ]:


try:
    all_data = pd.read_csv('all_data.csv')
except:
    all_data = pd.DataFrame()


# In[ ]:


all_data.tail()


# In[ ]:


y=0
while True:
    all_data = all_data.append(get_data(), ignore_index=True)
    all_data = all_data.drop_duplicates(keep='first')
    all_data.to_csv('all_data.csv', index=False)
    print(all_data.shape)
    data = {'api_key':'QEZAG779CCSVAYZ5', 'field2': all_data.shape[0]}
    thing_url ='https://api.thingspeak.com/update' #?api_key=QEZAG779CCSVAYZ5&field1=73
    requests.post(thing_url,data)
    y += 1
    if y%10 == 0:
        get_ipython().system('git pull')
        get_ipython().system('git add .')
        get_ipython().system('git commit -m "atualizando dados"')
        get_ipython().system('git push')
    sleep(180)

