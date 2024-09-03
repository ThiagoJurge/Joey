import requests
import re

# URLs e Headers
url = "https://api.z-api.io/instances/3D45F21828F6D0AC55D4DE7A807E3216/token/273FE76E3D2D7F6B181412C8/chats"
url_metadata = "https://api.z-api.io/instances/3D45F21828F6D0AC55D4DE7A807E3216/token/273FE76E3D2D7F6B181412C8/group-metadata/"
headers = {
    'Client-Token': 'F49c1fc59ca1a4e13abc1453618c6472bS',
    'Content-Type': 'application/json'
}

# Função para extrair números de 7 a 8 dígitos
def extract_numbers(text):
    return re.findall(r'\b\d{7,8}\b', text)

# Requisição para obter os grupos
response = requests.get(url, headers=headers).json()

# Iteração sobre os grupos
for data in response:
    if data["isGroup"]:
        # Extração dos números do name
        numbers = extract_numbers(data['name'])
        
        # Requisição do metadata para o grupo
        metadata = requests.get(f"{url_metadata}/{data['phone']}", headers=headers).json()
        
        # Extração dos números da description
        numbers += extract_numbers(metadata["description"])
        
        # Garantindo que os números sejam únicos
        unique_numbers = list(set(numbers))
        
        numbers_dict = {
            'name': data['phone'],
            'numbers': unique_numbers
        }
        print('-------')
        print(f"Phone: {data['phone']}, Group Info: {numbers_dict}")
