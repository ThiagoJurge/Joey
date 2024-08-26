import requests

url = "https://api.z-api.io/instances/3D43CEA9FCF000A02C7302172B1F54BB/token/C3FFE358EACBFC9BF0619541/send-text"

headers = {
    'Client-Token': 'F2723bf533e91476e9da2b6d27ab660a6S',
    'Content-Type': 'application/json'
}

payload = {
        "phone": "120363187127383452-group",
        "message": "Donovan me disse que vai pagar a rodada de pizza amanhã",
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)
