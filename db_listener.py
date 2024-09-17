import time
import requests
import base64
import re
from models.message_sender import MessageSender
from models.ZApiGroupExtractor import ZApiGroupExtractor
from services.db import execute_query  # Importa a função do arquivo separado

# Instância dos modelos
message_sender = MessageSender()
group_extraction = ZApiGroupExtractor()

def clean_entry(entry):
    """Limpa o texto removendo a tag #UPDT e conteúdo HTML."""
    cleaned_entry = entry.replace("#UPDT", "")
    cleaned_entry = re.sub(r'<hr>.*', '', cleaned_entry)
    return cleaned_entry.strip()

def process_attachments(anexos_result, grupo_phone):
    """Faz o download e envio dos anexos via WhatsApp."""
    for anexo in anexos_result:
        file_path = anexo[0]
        url = f"https://sga.altarede.com.br/storage/{file_path}"
        response = requests.get(url, verify=False)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if "image" in content_type:
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                base64_header = f"data:{content_type};base64,{image_base64}"
                message_sender.send_media(grupo_phone, base64_header, "image")
        else:
            print(f'Falha ao acessar o anexo: {response.status_code}')

def send_update_to_groups(chamado_id, designacao, clean_message, anexos_result):
    """Envia a atualização para os grupos apropriados, incluindo anexos."""
    designacao_id = group_extraction.extrair_designacao(designacao)
    
    for id in designacao_id:
        grupos = group_extraction.get_designacoes()
        for grupo in grupos:
            if id in str(grupo['designacoes']):
                mensagem = f"""*Chamado:* {chamado_id}
*Designação:* {designacao}
*Atualização:* {clean_message}"""
                message_sender.send_message(grupo["phone"], mensagem)

                # Envia anexos, se existirem
                if anexos_result:
                    process_attachments(anexos_result, grupo["phone"])

def process_new_entries(new_values):
    """Processa as novas entradas de chamados e envia as mensagens."""
    for value in new_values:
        if "#UPDT" in value[4]:
            try:
                circuito_id_result = execute_query(f'SELECT circuito_id FROM chamados WHERE id = {value[1]} AND status_id != 2')
                circuito_id = circuito_id_result[0][0] if circuito_id_result else None

                if circuito_id:
                    designacao_result = execute_query(f'SELECT designacao FROM circuitos WHERE id = {circuito_id}')
                    designacao = designacao_result[0][0] if designacao_result else None

                    anexos_result = execute_query(f'SELECT file_path FROM chamado_anexos WHERE chamado_observacao_id = {value[0]}')
                    
                    if designacao:
                        clean_message = clean_entry(value[4])
                        send_update_to_groups(value[1], designacao, clean_message, anexos_result)
            except Exception as e:
                print(f'Erro ao processar o chamado {value[1]}: {e}')

def main():
    """Função principal que monitora as atualizações no banco de dados."""
    last_id = None  # Inicializa o último ID monitorado

    while True:
        try:
            current_max_id_result = execute_query("SELECT MAX(id) FROM chamado_observacoes")
            current_max_id = current_max_id_result[0][0] if current_max_id_result and current_max_id_result[0][0] is not None else None

            if last_id is None:
                # Inicializa o last_id com o current_max_id no primeiro loop
                last_id = current_max_id
                print(f"Initial max ID found: {last_id}")
            elif current_max_id and current_max_id > last_id:
                # Busca por novos chamados com ID maior que last_id
                new_values = execute_query(f"SELECT * FROM chamado_observacoes WHERE id > {last_id}")
                
                if new_values:
                    process_new_entries(new_values)

                # Atualiza o last_id para o current_max_id atual
                last_id = current_max_id

        except Exception as e:
            print(f"Erro durante o loop principal: {e}")
        
        time.sleep(5)  # Espera 5 segundos antes de verificar novamente

if __name__ == "__main__":
    main()
