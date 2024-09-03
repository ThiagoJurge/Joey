import requests
import re
from config import Config


class ZApiGroupExtractor:
    def __init__(self):
        self.base_url = Config.NEW_API_URL
        self.headers = {
            "Client-Token": Config.CLIENT_TOKEN,
            "Content-Type": "application/json",
        }

    def extrair_designacao(self, text):
        """Extrai números de 7 a 8 dígitos de um texto."""
        return re.findall(r"\b\d{7,8}\b", text)

    def get_groups(self):
        """Obtém a lista de grupos via API."""
        url = f"{self.base_url}/chats"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_group_metadata(self, phone):
        """Obtém os metadados de um grupo específico."""
        url_metadata = f"{self.base_url}/group-metadata/{phone}"
        response = requests.get(url_metadata, headers=self.headers).json()
        return response

    def get_designacoes(self):
        """Processa os grupos e extrai números do name e description."""
        groups = self.get_groups()
        all_designacoes = []
        for group in groups:
            if group["isGroup"]:
                designacao = self.extrair_designacao(group["name"])
                metadata = self.get_group_metadata(group["phone"])
                designacao += self.extrair_designacao(metadata["description"])

                # Garantindo que os números sejam únicos
                designacoes = list(set(designacao))
                numbers_dict = {"phone": group["phone"], "designacoes": designacoes}
                all_designacoes.append(numbers_dict)

        return all_designacoes
