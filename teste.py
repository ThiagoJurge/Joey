import requests
import json

# URL do webhook que você deseja testar
webhook_url = 'https://187.16.255.94:9999/webhook-receiver'

# Payload de exemplo que será enviado no corpo da requisição
payload = {
    "senderLid": "552199999999",
    "phone": "552199999999",
    "text": {
        "message": "Esta é uma mensagem de teste via webhook."
    },
    "isGroup": False,
    "type": "ReceivedCallBack",
    "messageId": "ABCD1234",
    "photo": "https://example.com/user_photo.jpg",
    "status": "RECEIVED",
    "momment": 1625493600
}

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json'
}

# Função que envia a requisição POST para o webhook
def test_webhook():
    try:
        # Enviando a requisição POST
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
        # Verificando a resposta
        if response.status_code == 200:
            print(f"Sucesso! Webhook respondeu: {response.json()}")
        else:
            print(f"Erro ao enviar requisição: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Erro ao conectar ao webhook: {str(e)}")

# Executa o teste
if __name__ == '__main__':
    test_webhook()
