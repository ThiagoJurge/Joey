import mysql.connector
import time
from datetime import datetime, timedelta
from models.message_sender import MessageSender
from config import Config
from scripts.send_altarede_sistemas import encaminhar_os
from scripts.get_altared_sistemas_os import get_os_by_chamado
from scripts.send_google_form import send_form
#import schedule
import threading
import os, json
import requests

message_sender = MessageSender(Config.API_URL)

# Configuração do banco de dados
db_config = {
    "host": "187.16.255.97",
    "user": "read_donovan",
    "password": "D0D0,C@rl@",
    "database": "admin_noc",
}


class DatabaseMonitor:
    def __init__(self, config):
        self.config = config
        self.json_file = Config.GROUP_JSON_PATH

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        return mysql.connector.connect(**self.config)

    def fetch_results(self):
        """Executa a query e retorna os resultados."""
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, responsavel_id, status_id, data_agendada FROM chamados WHERE status_id != 2"
            )
            results = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro ao executar a consulta: {err}")
            results = []
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
        return results

    def format_results(self, results):
        """Formata os resultados para comparação."""
        formatted = []
        for row in results:
            chamado = row.get("id", "")
            responsavel_id = row.get("responsavel_id", "")
            status_id = row.get("status_id", "")
            data_agendada = (
                row["data_agendada"].strftime("%Y-%m-%d %H:%M:%S")
                if row.get("data_agendada")
                else ""
            )
            formatted.append((chamado, responsavel_id, status_id, data_agendada))
        return sorted(formatted)

    def get_responsavel_name(self, responsavel_id):
        """Obtém o nome do responsável a partir do ID."""
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True)
            query = """
                        SELECT nome, responsavel_type
                        FROM responsaveis 
                        WHERE id = %s
                    """
            cursor.execute(query, (responsavel_id,))
            result = cursor.fetchone()
            if result.get("responsavel_type") == "App\\Models\\Equipe":
                return result.get("nome")

        except mysql.connector.Error as err:
            print(f"Erro ao consultar o nome do responsável: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def get_status_chamado(self, status_id):
        """Obtém o status do chamado a partir do ID."""
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True)
            query = """
                    SELECT nome
                    FROM chamado_status 
                    WHERE id = %s
                """
            cursor.execute(query, (status_id,))
            result = cursor.fetchone()
            if result:
                nome = result.get("nome")
                if nome in ("Acionado", "Pendencia - Agendada"):
                    return nome
            return None  # Retorna None se o status não for encontrado ou não estiver na lista esperada

        except mysql.connector.Error as err:
            print(f"Erro ao consultar o status do chamado: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def read_json_file(self):
        with open(Config.FORM_DATA_PATH, "r") as file:
            return file.read()

    def write_json_file(self, data):
        with open(Config.FORM_DATA_PATH, "w") as file:
            file.write(data)

    def process_entries(self, chamado):
        json_data = self.read_json_file()

        # Converte a string JSON em um objeto Python
        entries = json.loads(json_data)

        # Filtra as entradas com o chamado especificado
        filtered_entries = [
            entry
            for entry in entries
            if int(entry["data"]["entry_825154660"]) == chamado
        ]

        if not filtered_entries:
            return (
                None,
                json_data,
            )  # Se não encontrar entradas com o chamado especificado, retorna None e o JSON original

        # Encontra a entrada mais recente
        latest_entry = max(
            filtered_entries, key=lambda x: datetime.fromisoformat(x["timestamp"])
        )

        # Remove todas as entradas com o chamado especificado
        remaining_entries = [
            entry
            for entry in entries
            if int(entry["data"]["entry_825154660"]) != chamado
        ]

        # Converte o objeto Python de volta para JSON string
        updated_json_data = json.dumps(remaining_entries, indent=4, ensure_ascii=False)

        self.write_json_file(updated_json_data)

        return latest_entry, updated_json_data

    def message_sender(
        self,
        message_type,
        chamado,
        responsavel_name,
        status_chamado,
        data_agendada,
        payload,
    ):

        groups = [
            {
                "equipe": "Equipe Infraestrutura 01",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Infraestrutura 02",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Angra",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Campos",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Lagos 01",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Lagos 02",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Linhares",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional NOF-01",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional NOF-02",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional NOF-03",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Paraty",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Petrópolis",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional RIO-01",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional RIO-02",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Vitória",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
            {
                "equipe": "Equipe Operacional Volta Redonda",
                "id_altarede_sistemas": "63",
                "id_marrera": "120363303090993469",
            },
        ]

        for item in groups:
            if item["equipe"] == responsavel_name:
                if message_type == "atividade_agendada":
                    self.schedule_message(
                        data_agendada,
                        item["id_marrera"],
                        f"`ACIONAMENTO RAT`\n\n*Protocolo:* {chamado}\n*Equipe:* {payload[0]['data']['entry_387529666']}\n*Cliente(s):*\n{payload[0]['data']['entry_1202092668']}",
                        chamado,
                        payload
                    )
                    # encaminhar_os(os, item["id_altarede_sistemas"])
                elif message_type == "equipe_acionada":
                    message_sender.send_message(
                        item["id_marrera"],
                        f"`ACIONAMENTO RAT`\n\n*Protocolo:* {chamado}\n*Equipe:* {payload[0]['data']['entry_387529666']}\n*Cliente(s):*\n{payload[0]['data']['entry_1202092668']}",
                    )
                    send_form(payload)
                    os = get_os_by_chamado(str(chamado))
                    # encaminhar_os(os, item["id_altarede_sistemas"])
                elif message_type == "no_rat":
                    message_sender.send_message(
                        item["id_marrera"],
                        f"A equipe {responsavel_name} não foi acionada no chamado {chamado}, pois o formulário não foi preenchido",
                    )
                else:
                    message_sender.send_message(
                        item["id_marrera"],
                        f"Não foi possivel gerar o acionamento para o chamado {chamado}",
                    )

    def process_changed_items(self, items):
        """Processa os itens que mudaram."""
        # Obtemos a entrada mais recente e seu status

        for item in items:
            chamado, responsavel_id, status_id, data_agendada = item
            responsavel_name = self.get_responsavel_name(responsavel_id)
            recent_entry_info = self.process_entries(chamado)
            if recent_entry_info[0] != None:
                if int(recent_entry_info[0]["data"]["entry_825154660"]) == chamado:
                    if responsavel_name:
                        status_chamado = self.get_status_chamado(status_id)
                        now = datetime.now()
                        # date_now = now.strftime("%Y-%m-%d %H:%M:%S")
                        if status_chamado == "Pendencia - Agendada":
                            if data_agendada:
                                self.message_sender(
                                    "atividade_agendada",
                                    chamado,
                                    recent_entry_info[0]["data"]["entry_387529666"],
                                    status_chamado,
                                    data_agendada,
                                    recent_entry_info,
                                )
                            else:
                                self.message_sender(
                                    "failed",
                                    chamado,
                                    recent_entry_info[0]["data"]["entry_387529666"],
                                    status_chamado,
                                    data_agendada,
                                    recent_entry_info,
                                )
                        elif status_chamado == "Acionado":
                            self.message_sender(
                                "equipe_acionada",
                                chamado,
                                recent_entry_info[0]["data"]["entry_387529666"],
                                status_chamado,
                                data_agendada,
                                recent_entry_info,
                            )
                        else:
                            self.message_sender(
                                "failed",
                                chamado,
                                recent_entry_info[0]["data"]["entry_387529666"],
                                status_chamado,
                                data_agendada,
                                recent_entry_info,
                            )
                #         # Aqui você pode adicionar qualquer lógica adicional, como enviar notificações ou atualizar o status
        else:
            self.message_sender(
                "no_rat",
                chamado,
                responsavel_name,
                "N/A",
                "N/A",
                "N/A",
            )

    def schedule_message(self, send_time, number, message, chamado, payload):
        """Agenda o envio de uma mensagem para um horário específico."""
        send_datetime = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
        delay = (send_datetime - datetime.now()).total_seconds()

        if delay > 0:
            threading.Timer(
                delay, lambda: (message_sender.send_message(number, message),
                                send_form(payload),
                                )
            ).start()
        else:
            message_sender.send_message(number, message)
            send_form(payload)

    def monitor_changes(self, interval=10):
        """Monitora mudanças na query em intervalos definidos."""
        previous_results = self.format_results(self.fetch_results())

        while True:
            time.sleep(interval)
            current_results = self.format_results(self.fetch_results())
            changed = set(current_results) - set(previous_results)

            if changed:
                self.process_changed_items(changed)

            previous_results = current_results


# Inicia o monitoramento de mudanças a cada 10 segundos
if __name__ == "__main__":
    monitor = DatabaseMonitor(db_config)
    monitor.monitor_changes(interval=10)
