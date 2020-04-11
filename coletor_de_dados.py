#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import requests
from time import sleep


# In[3]:


url  ='http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes'


# In[22]:


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


get_data()


# In[ ]:


try:
    all_data = pd.read_csv('all_data.csv')
except:
    all_data = pd.DataFrame()


# In[ ]:


all_data.tail()


# In[ ]:


'''y=0
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
        !git pull
        !git add .
        !git commit -m "atualizando dados"
        !git push
    sleep(180)
'''


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
            get_ipython().system('git pull')
            get_ipython().system('git add .')
            get_ipython().system('git commit -m "atualizando dados"')
            get_ipython().system('git push')
    break
    info = {'api_key':'QEZAG779CCSVAYZ5', 'field2': new_data.shape[0]}
    thing_url ='https://api.thingspeak.com/update'
    requests.post(thing_url,info)
    y += 1
    sleep(180)
    


# In[ ]:


new_data = get_data()


# In[ ]:


new_data.shape


# In[ ]:




