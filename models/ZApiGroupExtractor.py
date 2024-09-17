import requests
import re
import time
from typing import List, Dict  # Importando List e Dict do typing
from config import Config


class ZApiGroupExtractor:
    def __init__(self):
        self.base_url = Config.NEW_API_URL
        self.headers = {
            "Client-Token": Config.CLIENT_TOKEN,
            "Content-Type": "application/json",
        }
        self.max_retries = 3  # Número máximo de tentativas
        self.session = requests.Session()  # Usando uma sessão para melhorar a eficiência

    def extrair_designacao(self, text: str) -> List[str]:  # Usando List ao invés de list
        """Extrai números de 7 a 8 dígitos de um texto."""
        return re.findall(r"\b\d{7,8}\b", text)

    def make_request(self, url: str) -> Dict:  # Usando Dict ao invés de dict
        """Faz a requisição com retry em caso de falha."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx e 5xx
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                print(f"Tentativa {attempt + 1} falhou: Erro HTTP {http_err}")
            except requests.exceptions.RequestException as e:
                print(f"Tentativa {attempt + 1} falhou: {e}")
            time.sleep(2)  # Espera 2 segundos antes da próxima tentativa
        raise Exception("Número máximo de tentativas alcançado.")  # Levanta exceção se todas as tentativas falharem

    def get_groups(self) -> List[Dict]:  # Usando List e Dict para tipagem
        """Obtém a lista de grupos via API."""
        url = f"{self.base_url}/chats"
        return self.make_request(url)

    def get_group_metadata(self, phone: str) -> Dict:  # Usando Dict para tipagem
        """Obtém os metadados de um grupo específico."""
        url_metadata = f"{self.base_url}/group-metadata/{phone}"
        return self.make_request(url_metadata)

    def get_designacoes(self) -> List[Dict]:  # Usando List e Dict para tipagem
        """Processa os grupos e extrai números do name e description."""
        groups = self.get_groups()
        all_designacoes = []
        for group in groups:
            if group.get("isGroup", False):  # Verifica se a chave existe e é verdadeira
                designacao = self.extrair_designacao(group.get("name", ""))
                metadata = self.get_group_metadata(group.get("phone", ""))
                designacao += self.extrair_designacao(metadata.get("description", ""))

                # Garantindo que os números sejam únicos
                designacoes = list(set(designacao))
                numbers_dict = {"phone": group["phone"], "designacoes": designacoes}
                all_designacoes.append(numbers_dict)

        return all_designacoes
