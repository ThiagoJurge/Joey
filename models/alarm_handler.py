import re

class AlarmHandler:
    def __init__(self, group_fetcher, message_sender):
        # Inicializa o manipulador de alarmes com os objetos para buscar grupos e enviar mensagens
        self.group_fetcher = group_fetcher
        self.message_sender = message_sender

        # Padrões regex para identificar diferentes tipos de mensagens
        self.pattern_cliente = re.compile(r"\b\d{7,8}\b")  # Padrão para identificar números de clientes
        self.pattern_info = re.compile(r"INFO")  # Padrão para identificar mensagens de informações
        self.pattern_backbone = re.compile(r"(BB\-|OPS\-)")  # Padrão para identificar alarmes do backbone
        self.pattern_pps = re.compile(r"PPS\-")  # Padrão para identificar alarmes da PPS

    def process_message(self, message: str) -> str:
        # Processa a mensagem e decide o que fazer com base nos padrões identificados
        if self.pattern_info.search(message):
            return "Sensor de Info. No ACTION"  # Retorna sem ação para mensagens de info
        elif self.pattern_backbone.search(message):
            return self._handle_cliente_message(message, "backbone")  # Processa mensagens do backbone
        elif self.pattern_pps.search(message):
            return self._handle_cliente_message(message, "pps")  # Processa mensagens da PPS
        elif self.pattern_cliente.search(message):
            return self._handle_cliente_message(message, "cliente")  # Processa mensagens de clientes
        else:
            print(f"Não deu match em nada: {message}")
            return "No match found"  # Retorna quando nenhuma correspondência é encontrada

    def _send_message(self, group_id: str, message: str, message_type: str) -> dict:
        # Constrói a mensagem com base no tipo e envia para o grupo correspondente
        messages = {
            "backbone": f"*No momento o backbone abaixo está alarmado:*\n\n{message}",
            "pps": f"*No momento a PPS abaixo está alarmada:*\n\n{message}",
            "cliente": f"*Caro responsável*\nRecebemos o seguinte alarme em nosso equipamento:\n\n{message}"
        }

        # Envia a mensagem utilizando o message_sender e retorna a resposta
        response = self.message_sender.send_message(group_id, messages.get(message_type, message))
        return response

    def _get_designacoes_message(self, message: str) -> set:
        # Extrai e retorna todas as designações encontradas na mensagem usando o padrão de cliente
        return {match.group() for match in self.pattern_cliente.finditer(message)}

    def _handle_cliente_message(self, message: str, message_type: str) -> dict:
        # Carrega o mapeamento de designações do WhatsApp
        designacoes_whatsapp = self.group_fetcher.get_designacoes()

        # Extrai as designações da mensagem
        designacoes_message = self._get_designacoes_message(message)

        # Se o tipo de mensagem não for "cliente", envia a mensagem diretamente para o grupo padrão
        if message_type != "cliente":
            return self._send_message("120363187127383452-group", message, message_type)

        # Para cada match de designação, verifica se existe no mapeamento do WhatsApp e envia a mensagem
        for match in designacoes_message:
            for item in designacoes_whatsapp:
                if match in item["designacoes"]:
                    return self._send_message(item["phone"], message, message_type)

        # Caso nenhuma designação seja encontrada, retorna uma mensagem de erro
        print(f"Designações não encontradas para a mensagem: {message}")
        return {"status": "error", "message": "Designação não encontrada"}
