import re
from models.ZApiGroupExtractor import ZApiGroupExtractor

class AlarmHandler:
    def __init__(self, group_fetcher, message_sender):
        self.group_fetcher = group_fetcher
        self.message_sender = message_sender

        ### PATTERNS PARA DAR MATCH NO "TIPO DE DESINGAÇÃO ###
        self.pattern_cliente = re.compile(r"\b\d{7,8}\b")
        self.pattern_info = re.compile(r"INFO")
        self.pattern_backbone = re.compile(r"(BB\-|OPS\-)")
        self.pattern_pps = re.compile(r"PPS\-")

    def process_message(self, message: str) -> str:

        ### FUNÇÕES PRA VER EM QUAL PATTERN O SENSOR DA MATCH. ###
        ### SE NÃO DER MATCH EM NADA, A APLICAÇÃO NÃO VAI TOMAR NENHUMA DECISÃO ###
        if self.pattern_info.search(message):
            return "Sensor de Info. No ACTION"
        elif self.pattern_backbone.search(message):
            return self._handle_cliente_message(message, "backbone")
        elif self.pattern_pps.search(message):
            return self._handle_cliente_message(message, "pps")
        elif self.pattern_cliente.search(message):
            return self._handle_cliente_message(message, "cliente")
        else:
            print(f"Não deu match em nada: {message}")
            return "No match found"

    def _send_message(self, group_id: str, message: str, message_type: str) -> dict:
        ### FUNÇÃO CRIADA PARA PODER PROCESSAR O ENCAMINHAMENTO DAS MENSAGENS COM "TITULOS PERSONALIZADOS" ###
        messages = {
            "backbone": f"*No momento o backbone abaixo está alarmado:*\n\n{message}",
            "pps": f"*No momento a PPS abaixo está alarmada:*\n\n{message}",
            "cliente": f"*Caro responsável*\nRecebemos o seguinte alarme em nosso equipamento:\n\n{message}"
        }

        response = self.message_sender.send_message(group_id, messages.get(message_type, message))
        return response

    def _get_designacoes_message(self, message: str) -> set:
        ### FUNÇÃO QUE COMPARA A MENSAGEM DO SENSOR DO PRTG COM O PATTERN
        return {match.group() for match in self.pattern_cliente.finditer(message)}

    def _handle_cliente_message(self, message: str, message_type: str) -> dict:
        ### 
        designacoes_whatsapp = self.group_fetcher.get_designacoes()
        designacoes_message = self._get_designacoes_message(message)
        print(designacoes_whatsapp)

        if message_type != "cliente":
            return self._send_message("5522981013352", message, message_type)

        for match in designacoes_message:
            for item in designacoes_whatsapp:
                if match in item["designacoes"]:
                    return self._send_message(item["phone"], message, message_type)

        print(f"Designações não encontradas para a mensagem: {message}")
        return {"status": "error", "message": "Designação não encontrada"}

