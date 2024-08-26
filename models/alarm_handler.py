import re, json


"""Parte do programa para identificar se a requisição vem de cliente, pps ou backbone. 
No momento precisa ser adicionado manualmente nessa parte do código"""
class AlarmHandler:
    def __init__(self, group_fetcher, message_sender):
        self.group_fetcher = group_fetcher
        self.message_sender = message_sender
        self.pattern_cliente = re.compile(r"\b\d{7,8}\b")
        self.pattern_info = re.compile(r"INFO")
        self.pattern_backbone = re.compile(r"(BB\-|OPS\-)")
        self.pattern_pps = re.compile(r"PPS\-")

    def process_message(self, message):
        print(message)
        if self.pattern_info.search(message):
            return "Sensor de Info. No ACTION"
        elif self.pattern_backbone.search(message):
            return self.send_message("120363187127383452", message, "backbone")
        elif self.pattern_pps.search(message):
            return self.send_message("120363187127383452", message, "pps")
        elif self.pattern_cliente.search(message):
            return self.handle_cliente_message(message)
        else:
            print(f"Não deu match em nada: {message}")

    # Alertas Backbone 
    def send_message(self, group_id, message, message_type):
        if message_type == "backbone":
            message = f"*No momento o backbone abaixo está alarmado:*\n\n{message}"
        elif message_type == "pps":
            message = f"*No momento a PPS abaixo está alarmada:*\n\n{message}"
        elif message_type == "cliente":
            message = f"*Caro responsável*\nRecebemos o seguinte alarme em nosso equipamento:\n\n{message}"

        response = self.message_sender.send_message(group_id, message)
        return response
    
    ## Mapeamento de clientes ##
    def handle_cliente_message(self, message):
            # Carrega o mapeamento do JSON
            mapping = self.load_mapping()
            
            # Se o mapeamento é uma lista, você precisa iterar sobre cada item
            if isinstance(mapping, list):
                print('é lista')
                for sequencia in self.pattern_cliente.findall(message):
                    print(sequencia)
                    group_info = next((item for item in mapping if item.get('group_id') == sequencia), None)
                    if group_info:
                        group_id = group_info.get('group_id')
                        print(group_id)
                        return self.send_message(group_id, message, "cliente")
            else:
                # Se não for uma lista, assume que é um dicionário e funciona como antes
                for sequencia in self.pattern_cliente.findall(message):
                    print(sequencia)
                    group_info = mapping.get(sequencia)
                    if group_info:
                        group_id = group_info['group_id']
                        print(group_id)
                        return self.send_message(group_id, message, "cliente")
            
            return self.send_message("120363187127383452", message, "cliente")

    # abrir sempre o json mais atualizado #
    def load_mapping(self):
        with open('grupos.json', 'r') as file:
            return json.load(file)

