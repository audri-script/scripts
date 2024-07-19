from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# web
navegador = webdriver.Chrome()

# url
url_base = "https://www.amazon.com.br/s?k=amazon+iphone&adgrpid=127816894266&hvadid=593184216928&hvdev=c&hvlocphy=9196938&hvnetw=g&hvqmt=e&hvrand=6536095920832498801&hvtargid=kwd-6504762548&hydadcr=17282_13443039&tag=hydrbrgk-20&ref=pd_sl_9ga5qq32u3_e"

try:
    navegador.get(url_base)

    dados_produtos = []

    while True:
        # carregamento
        try:
            WebDriverWait(navegador, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "a-price-whole"))
            )
            WebDriverWait(navegador, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal"))
            )

            # preco inteir oe centavos
            elementos_precos_whole = navegador.find_elements(By.CLASS_NAME, "a-price-whole")
            elementos_precos_fraction = navegador.find_elements(By.CLASS_NAME, "a-price-fraction")
            
            # nome do produto
            elementos_nomes = navegador.find_elements(By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal")

            # consistencia
            if len(elementos_precos_whole) != len(elementos_precos_fraction) != len(elementos_nomes):
                raise ValueError("Número de elementos de preço e nomes não corresponde.")

            # extracao e limpeza 
            for i in range(len(elementos_precos_whole)):
                # indice
                if i < len(elementos_nomes):
                    valor_inteiro = elementos_precos_whole[i].text.replace('.', '').replace(',', '')
                    valor_fracao = elementos_precos_fraction[i].text.replace('.', '').replace(',', '')
                    # se valor_inteiro ou valor_fracao são vazios
                    if not valor_inteiro or not valor_fracao:
                        continue  # ignorar se não houver valor válido
                    valor_completo = f"{valor_inteiro}.{valor_fracao}"

                    try:
                        # converter pra float
                        preco_float = float(valor_completo)
                    except ValueError:
                        # se nao conseguir, avisar
                        print(f"Não foi possível converter para float: {valor_completo}")
                        continue

                    # extrai nome
                    nome_produto = elementos_nomes[i].text.strip()

                    # colocando na lista, no caso vira uma lista de tuplas
                    dados_produtos.append((nome_produto, preco_float))

            # link para a prox página
            try:
                link_proxima_pagina = WebDriverWait(navegador, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator"))
                )
                navegador.execute_script("arguments[0].scrollIntoView(true);", link_proxima_pagina)
                link_proxima_pagina.click()
                time.sleep(5)  # carregamento 5s
            except Exception as e:
                print("Não há mais páginas ou erro ao tentar acessar a próxima página:", e)
                break  # saindo do loop quando nao tem mais paginas

        except Exception as e:
            print("Erro ao tentar acessar elementos da página:", e)
            break  # sai do loop com erro

    # gerando a planilha csv
    nome_arquivo = "produtos_amazon.csv"
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # cabecalho
        escritor_csv.writerow(['Nome', 'Preço'])
        # dados
        for nome, preco in dados_produtos:
            escritor_csv.writerow([nome, f"R$ {preco:.2f}"])

    print(f"Dados exportados para '{nome_arquivo}'")

finally:
    # fechando navegador, fim
    navegador.quit()
