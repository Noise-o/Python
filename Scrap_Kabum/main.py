import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# Opções da janela 
op = Options()
op.add_argument('--width=400') # Firefox exige que defina altira e largura separadamente
op.add_argument('--height=800')
# op.headless = False
# op.add_argument('--headless') # dispensa a apresentação da janela


# Conexão com site  
url = 'https://www.kabum.com.br//'
driver = webdriver.Firefox(options=op)
driver.get(url)
# print(driver.page_source) # Abre as informações do nacegador criado pelo selenium
sleep(5) # Espera por 5 segundos até a execução da proxima linha 
soup = BeautifulSoup(driver.page_source, 'html.parser') # recebe as inforamaçoes do site aberto pelo seleniium 

# Buscando dados

element = driver.find_element('xpath', '//*[@id="input-busca"]') # Seleciona a busca do site 
element.send_keys('rtx')
element.submit()

sleep(2)

page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')

blocks = soup.findAll('div', attrs= {'class':'sc-bc1e5bbd-10 BhfWY'})

# Alocação em lista
_list = []

for block in blocks:
    title =  block.find('span', attrs={'class':'sc-d99ca57-0 kUQyzS sc-bc1e5bbd-15 LSdaP nameCard'})
    prazo = block.find('span', attrs={'class':'sc-3b515ca1-1 bXmdMv oldPriceCard'})
    a_vista = block.find('span', attrs={'class':'sc-3b515ca1-2 gybgF priceCard'})


    _list.append([title.text , a_vista.text[3:] , prazo.text[3:]])
   

    


data_frame = pd.DataFrame(_list, columns=['Produto', 'À vista', 'A prazo'])
print(data_frame)

# Loop entre páginas (Funfiona desde que o link esteja contido na href)

# def nextPage(soup):
#     page_swap  = soup.find('div', attrs= {'class':'sc-72859b2d-14 joZyYo'})
#     next= page_swap.find('li', {'class':'next'})


#     if next is False:
#         url = 'page'
#         skip = next.find('a', attrs= {'class':'nextLink'}, href= True)
#         url_final = (url + str(skip['href']))

#         return url_final
   

