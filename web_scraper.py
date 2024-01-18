# App Web Scraper

# Pacotes utilizados no projeto
import os
import re
import csv
import pickle
import requests
from bs4 import BeautifulSoup



# Definindo variável para página da Web
PAGE = "http://localhost:8000/index.html"


# Extraindo os dados
def extrai_dados(cb):

    # Extraindo o nome do carro
    str_name = cb.find('span', class_='car_name').text

    # Extraindo o número de cilindros e convertendo para int
    str_cylinders = cb.find('span', class_='cylinders').text
    cylinders = int(str_cylinders)

    # Tratando eventuais erros nos cilindros
    assert cylinders > 0, f"Espera - se que os cilindros sejam positivos e não {cylinders}"

    # Extraindo o peso do carro
    str_weight = cb.find('span', class_='weight').text

    # Tratando os dados e removendo as vírgulas
    weight = int(str_weight.replace(',', ''))

    # Tratando eventuais erros nos dados do peso
    assert weight > 0, f"Espera - se que o peso seja psitivo e não {weight}"

    # Extraindo a aceleração
    acceleration = float(cb.find('span', class_='acceleration').text)

    # Tratando eventuais erros nos dados da aceleração
    assert acceleration > 0, f"Espera - se que a aceleração seja positiva."
    
    # Gerando um dicinário para cada linha extraída
    linha = dict(name=str_name, cylinders=cylinders, weight=weight, acceleration=acceleration)
    return linha


def processa_blocos_carros(soup):
    
    # Extraindo informações de repetidas divisões
    car_blocks = soup.find_all('div', class_='car_block')

    # Criando a lista vazia para receber as linhas
    linhas = []

    # Loop pelos blocos de dados de carros
    for cb in car_blocks:
        linha = extrai_dados(cb)
        linhas.append(linha)
    
    print(f"\nTemos {len(linhas)} linhas de dados retornadas do scraping da página!")

    # Imprime a primeira e a última linha
    print("\nPrimeira linha copiada:")
    print(linhas[0])

    print("\nÚltima linha copiada:")
    print(linhas[-1])
    print("\n")

    # Gravando o resultado em csv
    with open("dados_copiados_v1.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames = linha.keys())
        writer.writeheader()
        writer.writerows(linhas)


# Execução principal do programa
if __name__ == "__main__":
    
    # Arquivo para guardar os dados copiados em cache
    filename = 'dados_copiados_v1.pickle'

    # Se o arquivo já existir, carregue o arquivo
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            print(f"\nCarregando o cache a partir do arquivo {filename}")
            result = pickle.load(f)
   
    # Se não, copie a página web
    else:
        print(f"\nCopiando dados da página {PAGE}.")
        result = requests.get(PAGE)
        with open(filename, 'wb') as f:
            print(f"\nGravando o cache em {filename}")
            pickle.dump(result, f)
    
    # Tratando eventuais erros no acesso a página Web
    assert result.status_code == 200, f"Obteve status {result.status_code} verifique sua conexão!"
    
    # Obtém o texto da página
    texto_web = result.text

    # Faz o parser do texto da página
    soup = BeautifulSoup(texto_web, 'html.parser')

    # Processa os dados de carros
    processa_blocos_carros(soup)



