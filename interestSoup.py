# cria um grafico com as informacoes sobre as taxas de juros de cada pais

import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

html_file = requests.get(r'https://www.global-rates.com/interest-rates/central-banks/central-banks.aspx') # fazendo donwload do codigo HTML
interestSoup = BeautifulSoup(html_file.content, 'html.parser') # criando um BeautifulSoup object
results = [] # vão vir valores que podemos não desejar, entre eles o None datatype, para isso vamos excluí-los dos nossos resultados
for tag in interestSoup.find_all('td'): # selecionando as tags que contém td
    if tag.string != None: # se a tag não tiver nenhuma string, ela retornará um valor None e para evitar de termos esse dado inutil, vamos retira-lo da nossa lista de resultados
        results.append(tag.string) # adiciona todas as tags td que tem strings dentro delas
results = results[8:-1] # excluindo dados inuteis no inicio
results = results[0:-26] # dados inuteis no final
pais, tx_atual, tx_anterior, data = [], [], [], [] # criando listas para armazenar as informações
for i in range(0, len(results), 4):
    pais.append(results[i])
    tx_atual.append(results[i+1][0:4]) # [0:4] selecionado para evitar problema de que o python não reconheça X.XXX % como um float
    tx_anterior.append(results[i+2][0:4])
    data.append(results[i+3])

df_juros = pd.DataFrame({'Pais': pais, 'Taxa de Juros Atual': tx_atual, 'Taxa de Juros Anterior': tx_anterior, 'Data': data}) # criando um data frame com as informações que foram adquiridas

print(df_juros.head()) # verificando as 5 primeiras linhas
df_juros['Taxa de Juros Atual'] = df_juros['Taxa de Juros Atual'].astype('float') # mudando tipo dos dados para float e datetime
df_juros['Taxa de Juros Anterior'] = df_juros['Taxa de Juros Anterior'].astype('float')
df_juros['Data'] = df_juros['Data'].astype('datetime64[ns]')
print(df_juros.info()) # verificando os tipos que cada dado é
plt.style.use('seaborn') # usando o estilo de grafico seaborn
plt.barh(df_juros['Pais'], df_juros['Taxa de Juros Atual']) # criando um grafico de barra horizontal para plotar as informacoes
plt.xlabel('Taxa de Juros (em %)') # mudando as legendas
plt.ylabel('Paises')
plt.title('Taxa de Juros Atual')
plt.xticks(np.arange(-1, 12, 0.5))
plt.show()
