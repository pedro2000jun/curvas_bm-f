import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def clean_data (str_in):
  aux = ""
  veri = 0
  str_in = str(str_in)
  for i in range (0, len(str_in)):
    if str_in[i] == '<':
      veri = 1
    elif str_in[i] == '>':
      veri = 0
    elif veri == 0 and str_in[i] != ' ' and str_in[i] != '\n':
      if str_in[i] == ',':
        aux = aux + '.'
      else:
        aux = aux + str_in[i]
      
  return float(aux)
    
def separate_data (vet, dc, base_252, base_360):
  i = 0
  while i <= len(vet)-2:
    dc.append(vet[i])
    base_252.append(vet[i+1])
    base_360.append(vet[i+2])
    i = i + 3

def adjust_data(obj):
  vet = []
  for i in obj:
    vet.append(clean_data(i))
  return vet


url = 'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/txref1.asp'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

dc = []
base_252 = []
base_360 = []

separate_data(adjust_data(soup.select('.tabelaConteudo1')), dc, base_252, base_360)  
separate_data(adjust_data(soup.select('.tabelaConteudo2')), dc, base_252, base_360)  
  
df = pd.DataFrame({'DC': dc, 'base_252': base_252, 'base_360': base_360})

df = df.sort_values(by=['DC'])

df.to_csv('curva.csv')
