from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import requests
import time
import re
import json

# Função para converter os dados para JSON
def convert_to_json(data):
    groups = []
    lines = data.strip().split('\n')
    for line in lines:
        # Ajustando regex para capturar IDs que podem conter hifens e nomes que não têm 'COPIAR ID' no final
        match = re.match(r"^\d+\s+([^\s]+)\s+(.+?)\s+COPIAR ID$", line)
        if match:
            group_id = match.group(1)
            group_name = match.group(2)
            groups.append({"group_id": group_id, "group_name": group_name})
    return json.dumps(groups, indent=4, ensure_ascii=False)


# Especificar o caminho para o Geckodriver
service = Service(executable_path="update/geckodriver")


# Configura o navegador Firefox para rodar em modo headless (sem abrir janela)
options = Options()
options.add_argument("--headless")

# Inicializa o WebDriver do Firefox
driver = webdriver.Firefox(service=service, options=options)

try:
    # Acessa a URL desejada
    driver.get("https://app.marrera.net/ferramentas/listargrupos/")
    
    # Aguarda o carregamento da página
    time.sleep(2)

    # Preenche o campo de e-mail
    first_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/form/div[1]/input')
    first_element.click()
    first_element.send_keys('donovan@altarede.com.br')

    # Aguarda um pouco após o clique
    time.sleep(1)

    # Preenche o campo de senha
    second_element = driver.find_element(By.XPATH, '//*[@id="inputPassword"]')
    second_element.click()
    second_element.send_keys('mudar@2024')

    # Aguarda um pouco após o clique
    time.sleep(1)

    # Clica no botão de login
    third_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/form/div[3]/div[2]/button')
    third_element.click()

    # Aguarda a página carregar após o login
    time.sleep(3)

    # Clica no botão para verificar a tabela
    click_verify = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div[1]/div/form/div/div[2]/button/i')
    click_verify.click()

    # Aguarda a tabela carregar
    time.sleep(12)

    # Extrai o texto da tabela
    table_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div[2]/div/div/div[2]')
    table_text = table_element.text

    # Converte os dados para JSON
    groups_json = convert_to_json(table_text)
    verify_len_table_text = len(table_text)

    #Verifica se a variavel é maior que 2000, parametro tirado que a table text tem 2573, para nunca escrever em branco e crashar o sistema
    if verify_len_table_text > 1000:
        # Atualiza o Json 
        print(groups_json)
        arq = open('/home/gabrielm/Lenny/grupos.json', 'w')
        arq.write(groups_json)
        arq.close()
    else:
        print('to aqui')
        url = "https://apiwt.marrera.net/send-message/id=oSAf5a3kxdrfQkjW"
        headers = {"Content-Type": "application/json"}
        payload = {"number": '5522997618608-1577397707', "textMessage": {"text": 'FALHA CRITICA: Erro na Rotina de atualizar os grupos do Lenny, verifica essa porra!'}}
        response = requests.post(url, json=payload, headers=headers, timeout=5)
           
finally:
    # Encerra o WebDriver
    driver.quit()