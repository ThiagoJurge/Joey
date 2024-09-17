import requests
import json
import re
from collections import Counter
import math
from multiprocessing import Pool, cpu_count
import time  # Importa biblioteca para medir tempo

class RipeQuery:
    def __init__(self):
        self.url_asn_verify = "https://stat.ripe.net/data/announced-prefixes/data.json?resource={}"

    ## Verifica os prefixos de cada ASN ##
    def verify_asn(self, asn):
        self.asn = asn
        # Formata o URL com o ASN fornecido
        url = self.url_asn_verify.format(asn)
        
        # Faz a requisição HTTP
        response = requests.get(url)
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Retorna o conteúdo JSON da resposta
            prefixes_json = response.json()
            prefixes_full = self.take_prefixes(prefixes_json)
            prefixes = self.verify_prefix(prefixes_full)
            
            # Usar multiprocessamento para verificar os prefixos
            with Pool(4) as pool:
                asn_data_list = pool.starmap(self.process_prefix, prefixes)
            
            # Combinar os resultados em um único dicionário
            asn_data = {}
            for data in asn_data_list:
                for prefix_with_mask, data_porcent_prefix in data.items():
                    # Se já houver dados para o prefixo, combine as porcentagens
                    if prefix_with_mask in asn_data:
                        asn_data[prefix_with_mask] = self.combine_asn_data(asn_data[prefix_with_mask], data_porcent_prefix)
                    else:
                        asn_data[prefix_with_mask] = data_porcent_prefix

            # Convertendo o dicionário final para uma lista de dicionários
            result = []
            for prefix, data in asn_data.items():
                # Remove ASNs com valor 0
                data = {asn: value for asn, value in data.items() if value != 0}
                
                # Só adiciona à lista final se houver dados de ASN (apaga origens sem ASN)
                if data:
                    item = {"Origin": prefix}
                    item.update(data)
                    result.append(item)

            return json.dumps(result, indent=4)

        else:
            return {"error": f"Failed to retrieve data, status code: {response.status_code}"}

    ## Processa cada prefixo individualmente ##
    def process_prefix(self, prefix, mask):
        prefix_path = self.get_url(prefix, mask)
        asn_data = {}
        if prefix_path:
            as_paths = prefix_path.get('As Path')
            prefix_with_mask = f"{prefix}/{mask}"
            data_porcent_prefix = self.verify_left_asn(prefix_with_mask, as_paths)
            
            if data_porcent_prefix:
                asn_data[prefix_with_mask] = data_porcent_prefix
        return asn_data

    ## Tratar o JSON e retornar os prefixos ##
    def take_prefixes(self, data_json):
        try:
            prefixes = [item['prefix'] for item in data_json['data']['prefixes']]
            return prefixes
        except:
            return {"error": f"Falha ao tentar extrair os prefixos com os dados imputados abaixo:\n {data_json}"}

    def verify_prefix(self, prefixes):
        divided_prefixes = [(item.split('/')[0], item.split('/')[1]) for item in prefixes]
        return divided_prefixes
    
    def get_url(self, prefix, mask):  # Função para pegar os dados de as path do prefixo #
        url = f"https://stat.ripe.net/data/looking-glass/data.json?resource={prefix}%2F{mask}&starttime=now"
        url_response = requests.get(url)
        if url_response.status_code == 200:
            path_atributes = url_response.json()
            as_paths = [peer['as_path'] for rrc in path_atributes['data']['rrcs'] for peer in rrc['peers']]
            PathPrefix = {"Prefixo": prefix, "As Path": as_paths}
            return PathPrefix
        return None
    
    def verify_left_asn(self, prefix, aspath):
        asn_left_of_customer = []
        
        # Itera sobre os as-paths e extrai o ASN à esquerda de self.asn
        for path in aspath:
            asn_list = path.split()  # Divide o as-path em uma lista de ASNs
            if self.asn in asn_list:  # Verifica se o ASN está presente no as-path
                index_asn = asn_list.index(self.asn)
                if index_asn > 0:  # Verifica se há um ASN à esquerda do ASN alvo
                    asn_left_of_customer.append(asn_list[index_asn - 1])
        
        # Contabiliza as ocorrências e calcula as porcentagens
        total = len(asn_left_of_customer)
        if total == 0:
            return {}  # Retorna um dicionário vazio se não houver ASNs à esquerda
        else:
            # Conta a ocorrência de cada ASN
            asn_counts = Counter(asn_left_of_customer)
            
            # Calcula a porcentagem de cada ASN
            asn_percentage = {asn: (asn_left_of_customer.count(asn) / total) * 100 for asn in asn_left_of_customer}
            
            # Arredonda as porcentagens
            asn_percentage = {asn: self.custom_round(percentage) for asn, percentage in asn_percentage.items()}
            
            return asn_percentage

    def combine_asn_data(self, original, new_data):
        for asn, percentage in new_data.items():
            if asn in original:
                original[asn] = max(original[asn], percentage)
            else:
                original[asn] = percentage
        return original

    # Função para arredondar valores, mas se o valor for menor que 5, irá arredondar para 0. 
    def custom_round(self, value):
        if value < 10: 
            return 0
        return math.ceil(value)