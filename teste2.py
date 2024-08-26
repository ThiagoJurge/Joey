import requests

url = "https://api.z-api.io/instances/3D45F21828F6D0AC55D4DE7A807E3216/token/273FE76E3D2D7F6B181412C8/chats"

headers = {
    'Client-Token': 'F49c1fc59ca1a4e13abc1453618c6472bS',
    'Content-Type': 'application/json'
}




response = requests.get(url, headers=headers).json()

for data in response:
    if data["isGroup"] == True:
        print(data["phone"], data["name"])
