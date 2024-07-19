from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# abre navegador
navegador = webdriver.Chrome()

# url da pagina 
url_base = "https://coinmarketcap.com/pt-br/currencies/bitcoin/"
navegador.get(url_base)

# obtendo elemento html com preco do ativo
def obter_preco():
    try:
        # Esperar o carregamento do preço
        preco_elemento = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-d1ede7e3-0.hSTakI.base-text"))
        )
        preco = preco_elemento.text
        return preco
    except Exception as e:
        print(f"Erro ao obter o preço: {e}")
        return None

# obtendo elemento html com o nome do ativo
def obter_nome():
    try:
        # esperar o carregamento do nome do ativo
        nome_elemento = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-d1ede7e3-0.bEFegK"))
        )
        nome = nome_elemento.text
        return nome
    except Exception as e:
        print(f"Erro ao obter o nome do ativo: {e}")
        return None

# loop coleta
while True:
    nome = obter_nome()
    preco = obter_preco()
    if nome and preco:
        print(f"Ativo: {nome} - Preço do Bitcoin: {preco}")
        # Salvar o nome e o preço em um arquivo CSV
        with open("precos_bitcoin.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), nome, preco])
    else:
        print("Não foi possível obter o nome ou o preço.")

    # intervalo atualizacao 
    time.sleep(5)
