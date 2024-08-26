import json, requests

def send_form(json_data):
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSfaF2FvkWTqJrU6foWO4nSujtX4vjwmhjLDNohvQMTlAT0_Wg/formResponse"
    # print(json_data)
    url = (
        #f"{base_url}?entry.825154660={json_data[0]["data"]["entry_825154660"]}"
        #f"&entry.387529666={json_data[0]["data"]["entry_387529666"]}"
        #f"&entry.1071483611={json_data[0]["data"]["entry_1071483611"]}"
        #f"&entry.2130349081={json_data[0]["data"]["entry_2130349081"]}"
        #f"&entry.1932602901={json_data[0]["data"]["entry_1932602901"]}"
        #f"&entry.313095559={json_data[0]["data"]["entry_313095559"]}"
        #f"&entry.1202092668={json_data[0]["data"]["entry_1202092668"]}"
    )

    response = requests.get(url)
    print(response)
    return url
