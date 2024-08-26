import requests
from bs4 import BeautifulSoup

def get_os_by_chamado(chamado_value):
    # URL da requisição
    url = "https://corporate.altaredesistemas.com.br/altarede/pagina.php?secao=pesquisa_os_aberto&form_destino=cadastro_os"

    # Headers da requisição
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=neiodrbbolbr1mr1u3cp15vir0",
        "Referer": "https://corporate.altaredesistemas.com.br/altarede/pagina.php?secao=home_suporte",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    # Fazendo a requisição
    response = requests.get(url, headers=headers)

    # Parseando o HTML com BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrando a tabela com o id 'example'
    table = soup.find('table', {'id': 'example'})

    # Extraindo os dados da tabela e convertendo em um dicionário
    if table:
        # Encontrando os headers da tabela
        headers = [header.text.strip() for header in table.find_all('th')]
        
        # Encontrando os índices das colunas "chamado" e "O.S."
        try:
            chamado_index = headers.index("Chamado")
            os_index = headers.index("O.S.")
        except ValueError:
            return "not_found"

        # Procurando o valor do chamado na tabela
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == len(headers) and cells[chamado_index].text.strip() == chamado_value:
                return cells[os_index].text.strip()
    
    return "not_found"