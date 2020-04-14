#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('python -m pip install -r requirements.txt')


# In[3]:


import pandas as pd
import requests
from time import sleep


# In[4]:


url  ='http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes'


# In[5]:


def get_data():
    try:
        data = requests.get(url).json()
        df = pd.DataFrame.from_records(data['DATA'], columns=data['COLUMNS'])
        df['DATAHORA'].apply(lambda x: pd.datetime.strptime(x, "%m-%d-%Y %H:%M:%S"))
        df['DATAHORA'] = pd.to_datetime(df['DATAHORA'], errors='coerce')
        return df
    except:
        return pd.DataFrame()


# In[ ]:


y=0
while True:
    new_data = get_data()
    if new_data.shape[0] >0:
        datas = list(new_data.DATAHORA.dt.date.unique())
        for data in datas:
            filename = "data/"+str(data)+".csv"
            try:
                d = pd.read_csv(filename, parse_dates = ['DATAHORA'])
            except:
                d = pd.DataFrame()

            d2 = d.append(new_data[new_data.DATAHORA.dt.date == data], ignore_index=True)
            d2 = d2.drop_duplicates(keep='first')
            d2.to_csv(filename, index=False)


        if y%10 == 0:
            #!git pull
            get_ipython().system('git add .')
            get_ipython().system('git commit -m "atualizando dados"')
            get_ipython().system('git push')
    info = {'api_key':'QEZAG779CCSVAYZ5', 'field2': new_data.shape[0]}
    thing_url ='https://api.thingspeak.com/update'
    requests.post(thing_url,info)
    y += 1
    for _ in range(18):
        print('.', end='', flush=True)
        sleep(10)
    

