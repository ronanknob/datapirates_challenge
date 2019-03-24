# Data Pirates challenge

Forked from: https://github.com/NeowayLabs/jobs/blob/master/datapirates/challengePirates.md

## Visão geral
O projeto é constituído por uma aplicação em Python que faz scraping da página dos correios especificada. Primeiro, ela faz um craping da página e obtém uma lista das UF's que existe na página. Com essa lista, executa um loop. Cada iteração deste loop pesquisa um dos elementos da lista de UF's, obtém os atributos "localidade" e "faixa de cep", inserindo-os em forma de tupla num array. Por fim, os elementos são impressos em um arquivo jsonl na pasta raiz da aplicação.

## Requisitos:
* Debian (para uso do Chrominum - Utilizei Ubuntu);
* Python 3.6;
* Navegador Chrominum;
* Pycharm (utilizada versão 2018.3 Community);
* pip (para instalação de pacotes sugeridos) e pacotes: 
	* selenium;
	* Beautifulsoup; 
	* requests;
	* jsonlines.

## Como Utilizar
* Fazer a cópia do projeto a partir do repositório;
* No Pycharm, carregar o projeto (File -> Open) e navegar até o path;
* Na classe app.py, clique com o botão direito e selecione a opção Run'app'
* Visualizar o arquivo de output com algum editor ou pela IDE. O arquivo será criado na pasta raiz (certifique-se de ter acessos apropriados para que ele seja criado)

### Observações:
* Na linha 39 está fixado o range para imprimir resultados de 2 estados, como pedido no teste. Como existe um array com todos os valores de estado, caso o numero 2 como argumento do for seja alteado para len(lista_estados), o programa faz a coleta de dados para todos os estados
* OBS: O navegador Chrominum será aberto algumas vezes automaticamente pelo Webdriver para navegação durante o processo.
* Algumas localidades tem dois registros no arquivo de output. Isso acontece devido a haver a mesma faixa de CEP para dois Tipos de faixa diferentes. As vezes a faixa é igual, as vezes não. Esse detalhe não foi tratado nesta aplicação.


