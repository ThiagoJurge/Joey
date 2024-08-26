import requests

def encaminhar_os(codigo, cod_tecnico):
    url = "https://corporate.altaredesistemas.com.br/altarede/controller_encaminhamento.php"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PHPSESSID=neiodrbbolbr1mr1u3cp15vir0",
        "Origin": "https://corporate.altaredesistemas.com.br",
        "Referer": "https://corporate.altaredesistemas.com.br/altarede/pagina.php?secao=pesquisa_os_aberto&form_destino=cadastro_os",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    data = {
        "action": "encaminhar",
        "codigo": codigo,
        "cod_tecnico": cod_tecnico,
        "tipo": "OS",
        "cod_cliente": "1.16",
        "motivo": ""
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()
