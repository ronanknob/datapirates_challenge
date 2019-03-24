# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests

# Construindo tabela de UF's com base na disponibilizada no site
# obtendo dados do endereço
r = requests.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")

# scraping com Beautiful Soup
soup = BeautifulSoup(r.text, 'html.parser')

# extraindo a lista de estados da página
results = soup.find_all('select', attrs={'class': 'f1col'})

# Extraindo e tratando a string com os estados
# Obtendo resultado da lista
estados = results[0]
#  Extraindo texto sem tag e convertendo para string
estados = str(estados.find("option").text)
#  Removendo caracteres nulos no início e fim
estados = estados.strip(" ")

# Populando uma lista com estados
lista_estados = []
estados_tam = len(estados)
for x in range(0, estados_tam, 3):
    lista_estados.append(estados[x:x + 2])

# inicia o driver do Chrominum
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

# acessa o site e aguarda 2s para carregamento
driver.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")
time.sleep(2)

# Seleciona o elemento de UF e depois seleciona o estado
seletor_uf = Select(driver.find_element_by_name("UF"))
seletor_uf.select_by_visible_text(lista_estados[0])

# Clica em Buscar
driver.find_element_by_xpath("//*[@id='Geral']/div/div/div[4]/input").click()
