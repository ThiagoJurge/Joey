import requests

class MessageSender:
    def __init__(self, api_url):
        self.api_url = api_url
        self.headers = {"Content-Type": "application/json"}

    def send_message(self, number, message):
        payload = {"number": number, "textMessage": {"text": message}}
        # print(payload)
        # print(number)
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=5)
            # print(response)
            return response.json()
        except:
            return "Falha no encaminhamento da mensagem"
        # return number
