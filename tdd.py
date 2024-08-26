import requests

url = "http://localhost:81/send_message"

headers = {
    "User-Agent": "PostmanRuntime/7.41.0",
    "Accept": "/",
    "Postman-Token": "2761180d-42c1-4067-b74b-866e48b20f9a",
    "Host": "localhost:81",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = """
C.G.R Altarede Corporate

Equipamento: ARC-CPG_1.1
Sensor: (ten-gigabit-ethernet-1/1/1) AN-(18200034)-]12001096-]ARC-PDM_1.1 Traffic
Status: TESTE DE INTEGRIDADE AUTOMATICO DO LENNY, POR FAVOR DESCONSIDERAR
"""

try:
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Verifica se houve algum erro na requisição
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print("Error:",e)