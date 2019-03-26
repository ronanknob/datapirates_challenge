# coding=utf-8
import time

import stringify as stringify
from jsonlines.jsonlines import ReaderWriterBase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import math
import jsonlines
import FaixaCep
import json

# Lista final que guardará as tuplas de resultado
registros_arr = []
# Inserindo primeira tupla (pode ser usada como cabeçalho no import)

# Construindo tabela de UF's com base na disponibilizada no site
# obtendo dados do endereço
r = requests.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm", allow_redirects=False)
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

# ------ INICIA CRAPING ------------
for x in range(0, 2, 1):  # Executa com as primeiras 2 UF's da lista
    # inicia o driver do Chrominum
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    # acessa o site e aguarda 1s para carregamento da página
    driver.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")
    time.sleep(1)

    # Seleciona o elemento de UF e depois seleciona o estado
    seletor_uf = Select(driver.find_element_by_name("UF"))
    seletor_uf.select_by_visible_text(lista_estados[x])

    # Clica em Buscar
    driver.find_element_by_xpath("//*[@id='Geral']/div/div/div[4]/input").click()

    '''
    Aqui estou coletando os dados da tabela na página resultado. Como há duas tabelas com mesmo nome, 
    uma trazendo o estado resultado, e outra trazendo os resultados em si, escolhi o elemento que contém
    as duas tabelas para fazer o parse.
    '''
    dados = driver.find_element_by_class_name("ctrlcontent")
    html = dados.get_attribute('outerHTML')

    # Executa BeautifulSoup para fazer o parser desse HTML
    soupDados = BeautifulSoup(html, "html.parser")

    # Obtem o total de páginas de resultado para checar se há mais de uma.
    qt_paginas = soupDados.text
    qt_paginas = int(qt_paginas[qt_paginas.find("de") + 3:qt_paginas.find("de") + 7])
    if qt_paginas >= 50:
        qt_paginas = math.ceil(qt_paginas / 50)  # valor inteiro antecessor mais próximo
    else:
        qt_paginas = 1

    if qt_paginas == 1:  # se existe apenas 1 página, roda apenas 1 vez
        # Obtendo os dois elementos tmptabela presentes na página
        tabelas = soupDados.find_all("table", attrs={'class': 'tmptabela'})

        # Selecionando apenas a tabela correta
        tabela_localidades = tabelas[1]

        # Guardando nome das localidades numa lista
        localidades = tabela_localidades.find_all('td', attrs={'width': '100'})
        faixas = tabela_localidades.find_all('td', attrs={'width': '80'})

        total_linhas = len(faixas)  # faixas não possui repetições
        localidades_pos = 0
        faixas_pos = 0
        for z in range(0, total_linhas, 1):
            trim_faixas = str(faixas[faixas_pos].text)
            trim_faixas = trim_faixas.strip(" ")
            faixacep = FaixaCep.FaixaCep(lista_estados[x], localidades[localidades_pos].text, trim_faixas)
            # tupla = (lista_estados[x], localidades[localidades_pos].text, trim_faixas)
            registros_arr.append(faixacep)  # Incremento na lista global
            localidades_pos = localidades_pos + 2  # incrementa dois para pular informação de situação
            faixas_pos = faixas_pos + 1
    else:
        for y in range(0, qt_paginas, 1):
            # Obtendo os dois elementos tmptabela presentes na página
            tabelas = soupDados.find_all("table", attrs={'class': 'tmptabela'})

            # Selecionando apenas a tabela correta
            tabela_localidades = tabelas[len(tabelas) - 1]

            # Guardando nome das localidades numa lista
            localidades = tabela_localidades.find_all('td', attrs={'width': '100'})
            faixas = tabela_localidades.find_all('td', attrs={'width': '80'})

            total_linhas = len(faixas)  # faixas não possui repetições
            localidades_pos = 0
            faixas_pos = 0
            for z in range(0, total_linhas, 1):
                trim_faixas = str(faixas[faixas_pos].text)
                trim_faixas = trim_faixas.strip(" ")
                trim_faixas = trim_faixas.strip(" ")
                faixacep = FaixaCep.FaixaCep(lista_estados[x], localidades[localidades_pos].text, trim_faixas)
                # tupla = (lista_estados[x], localidades[localidades_pos].text, trim_faixas)
                registros_arr.append(faixacep)  # Incremento na lista global
                localidades_pos = localidades_pos + 2  # incrementa dois para pular informação de situação
                faixas_pos = faixas_pos + 1

            if y <= qt_paginas - 2:  # Só executa o click em próxima página até a penúltima página.
                # Vai para próxima paǵina
                url_proxima = "javascript:document.Proxima.submit('Proxima')"
                driver.find_element_by_xpath('//a[@href="' + url_proxima + '"]').click()
                # Espera para carregar os dados da página
                time.sleep(2)
                # Atualiza dados das variáveis
                dados = driver.find_element_by_class_name("ctrlcontent")
                html = dados.get_attribute('outerHTML')
                # Executa BeautifulSoup para fazer o parser desse HTML
                soupDados = BeautifulSoup(html, "html.parser")
    # Fecha o Chrominum
    driver.close()

# Fazer o export da lista para um JSONL
with jsonlines.open('./output.jsonl', mode='w') as writer:
    for i in range(0, len(registros_arr), 1):
        writer.write(vars(registros_arr[i]))
writer.close()
