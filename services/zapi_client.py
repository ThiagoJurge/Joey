import requests
from config import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.NEW_API_URL
        self.headers = {
            "Client-Token": Config.CLIENT_TOKEN,
            "Content-Type": "application/json",
        }

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
