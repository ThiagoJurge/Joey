import mysql.connector
import time
import requests
import base64
import re
from models.message_sender import MessageSender
from models.ZApiGroupExtractor_teste import ZApiGroupExtractor

message_sender = MessageSender()
group_extraction = ZApiGroupExtractor()

# Dados de conexão ao banco de dados
db_config = {
    'host': '187.16.255.97',
    'user': 'read_donovan',
    'password': 'D0D0,C@rl@',
    'database': 'admin_noc'
}

# Função para conectar ao banco de dados
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Função para executar uma consulta SQL
def execute_query(query):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Obtém todos os resultados
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def clean_entry(entry):
    # Remove a string #UPDT
    cleaned_entry = entry.replace("#UPDT", "")
    
    # Remove qualquer HTML e seu conteúdo usando regex
    cleaned_entry = re.sub(r'<hr>.*', '', cleaned_entry)
    
    # Remover espaços extras
    return cleaned_entry.strip()

def main():
    last_id = None  # Armazena o último ID monitorado

    while True:
        current_max_id_result = execute_query("SELECT MAX(id) FROM chamado_observacoes")
        current_max_id = current_max_id_result[0][0] if current_max_id_result and current_max_id_result[0][0] is not None else None

        if last_id is None:
            # No primeiro loop, inicializa last_id com o current_max_id
            last_id = current_max_id
            print(f"Initial max ID found: {last_id}")
        else:
            # Verifica se o current_max_id é maior que o last_id
            if current_max_id and current_max_id > last_id:
                new_values = execute_query(f"SELECT * FROM chamado_observacoes WHERE id > {last_id}")
                
                if new_values:  # Verifica se há novos valores
                    for value in new_values:
                        if "#UPDT" in value[4]:
                            print(value)
                            try:
                                circuito_id_result = execute_query(f'SELECT circuito_id FROM chamados WHERE id = {value[1]} AND status_id != 2')
                                circuito_id = circuito_id_result[0][0] if circuito_id_result else None
                                
                                designacao_result = execute_query(f'SELECT designacao FROM circuitos WHERE id = {circuito_id}')
                                designacao = designacao_result[0][0] if designacao_result else None

                                anexos_result = execute_query(f'SELECT file_path FROM chamado_anexos WHERE chamado_observacao_id = {value[0]}')
                                
                            except Exception as e:
                                print(f'Erro ao processar o chamado {value[1]}: {e}')
                                continue  # Continua com o próximo chamado em caso de erro

                            if designacao:
                                designacao_id = group_extraction.extrair_designacao(designacao)

                                for id in designacao_id:
                                    grupos = group_extraction.get_designacoes()
                                    for grupo in grupos:
                                        if id in str(grupo['designacoes']):
                                            atualizacao = value[4]
                                            mensagem = f"""*Chamado:* {value[1]}
*Designação:* {designacao}
*Atualização:* {clean_entry(value[4])}"""
                                            message_sender.send_message(grupo["phone"], mensagem)
                                                
                                            if anexos_result:
                                                for anexo in anexos_result:
                                                    # Acessa o primeiro elemento da tupla
                                                    file_path = anexo[0]
                                                    url = f"https://sga.altarede.com.br/storage/{file_path}"
                                                    response = requests.get(url, verify=False)
                                                    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                                                        content_type = response.headers.get('Content-Type')
                                                        # print(response.text)
                                                        if "image" in content_type:
                                                            image_base64 = base64.b64encode(response.content).decode('utf-8')
                                                            base64_header = f"data:{content_type};base64,{image_base64}"
                                                            message_sender.send_media(grupo["phone"], base64_header, "image")


                                                    else:
                                                        print(f'Falha ao acessar o anexo: {response.status_code}')

                            
                        last_id = current_max_id  # Atualiza last_id

        # Espera 5 segundos antes de verificar novamente
        time.sleep(5)

# Execução do script
if __name__ == "__main__":
    main()

