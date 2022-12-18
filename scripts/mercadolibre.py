import requests
import pandas as pd
from bs4 import BeautifulSoup

url_base = 'https://lista.mercadolivre.com.br/'
produto_nome = input('Qual produto você deseja? ')
response = requests.get(url_base + produto_nome)
site = BeautifulSoup(response.text, 'html.parser')
produtos = site.findAll('li', attrs={'class': 'ui-search-layout__item shops__layout-item'})
df = pd.DataFrame()
for produto in produtos:
    titulo = produto.find('h2', attrs={'class': 'ui-search-item__title'})
    link = produto.find('a', attrs={'class': 'ui-search-link'})

    real = produto.find('span', attrs={'class': 'price-tag-fraction'})
    real = real.text.replace('.', '')
    centavos = produto.find('span', attrs={'class': 'price-tag-cents'})
    if(centavos):
        preco = real + '.' + centavos.text
    else:
        preco = real
    row = pd.DataFrame(
        data=[{
        'produto': titulo.text, 
        'link':  link['href'],
        'preco': preco
        }], columns=['produto', 'link', 'preco'])
    df = pd.concat([df, row], ignore_index=True)
filename = produto_nome + '.csv'
df.to_csv(filename, sep=';')
