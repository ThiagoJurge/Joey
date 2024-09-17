import requests
from config import Config


class MessageSender:
    def __init__(self, api_url=None):
        self.api_url = Config.NEW_API_URL
        self.headers = {
            "Client-Token": Config.CLIENT_TOKEN,
            "Content-Type": "application/json",
        }

    def send_message(self, number, message):
        payload = {"phone": number, "message": message}
        url = f"{self.api_url}/send-text"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Verifica se houve algum erro HTTP
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Exibe a mensagem de erro HTTP
            return f"Falha no encaminhamento da mensagem: HTTP error {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            print(
                f"Connection error occurred: {conn_err}"
            )  # Exibe a mensagem de erro de conexão
            return "Falha no encaminhamento da mensagem: erro de conexão"
        except requests.exceptions.Timeout as timeout_err:
            print(
                f"Timeout error occurred: {timeout_err}"
            )  # Exibe a mensagem de erro de timeout
            return "Falha no encaminhamento da mensagem: tempo de conexão esgotado"
        except requests.exceptions.RequestException as req_err:
            print(
                f"An error occurred: {req_err}"
            )  # Exibe uma mensagem genérica para outros erros de requests
            return "Falha no encaminhamento da mensagem: erro na requisição"
        except ValueError as json_err:
            print(
                f"JSON decode error: {json_err}"
            )  # Exibe a mensagem de erro de decodificação JSON
            return "Falha ao processar a resposta: erro ao decodificar o JSON"
        except Exception as e:
            print(
                f"An unexpected error occurred: {e}"
            )  # Exibe uma mensagem genérica para qualquer outro tipo de exceção
            return "Falha no encaminhamento da mensagem: erro inesperado"
        
    def send_media(self, number, media_link, mediatype):
        # print(media_link)
        
        payload = {"phone": number, "image": media_link}
        url = f"{self.api_url}/send-image"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Verifica se houve algum erro HTTP
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Exibe a mensagem de erro HTTP
            return f"Falha no encaminhamento da mensagem: HTTP error {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            print(
                f"Connection error occurred: {conn_err}"
            )  # Exibe a mensagem de erro de conexão
            return "Falha no encaminhamento da mensagem: erro de conexão"
        except requests.exceptions.Timeout as timeout_err:
            print(
                f"Timeout error occurred: {timeout_err}"
            )  # Exibe a mensagem de erro de timeout
            return "Falha no encaminhamento da mensagem: tempo de conexão esgotado"
        except requests.exceptions.RequestException as req_err:
            print(
                f"An error occurred: {req_err}"
            )  # Exibe uma mensagem genérica para outros erros de requests
            return "Falha no encaminhamento da mensagem: erro na requisição"
        except ValueError as json_err:
            print(
                f"JSON decode error: {json_err}"
            )  # Exibe a mensagem de erro de decodificação JSON
            return "Falha ao processar a resposta: erro ao decodificar o JSON"
        except Exception as e:
            print(
                f"An unexpected error occurred: {e}"
            )  # Exibe uma mensagem genérica para qualquer outro tipo de exceção
            return "Falha no encaminhamento da mensagem: erro inesperado"
