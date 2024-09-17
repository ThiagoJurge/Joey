from flask import Blueprint, request, jsonify
from models.message_sender import MessageSender
from config import Config
# from teste import get_bgp_items_by_asn
import requests, re


webhook_zapi = Blueprint("webhook_zapi", __name__)
# message_sender = MessageSender()


# def get_group_metadata(phone):
#     """Obtém os metadados de um grupo específico."""
#     base_url = Config.NEW_API_URL
#     headers = {
#         "Client-Token": Config.CLIENT_TOKEN,
#         "Content-Type": "application/json",
#     }
#     url_metadata = f"{base_url}/group-metadata/{phone}"
#     response = requests.get(url_metadata, headers=headers).json()
#     return response["description"]

# def extract_as_numbers(text):
#     # Regex to match "AS" followed by digits
#     pattern = r'AS(\d+)'

#     # Find all matches in the entire text
#     matches = re.findall(pattern, text)

#     return matches



# @webhook_zapi.route("//webhook-receiver", methods=["POST"])
# def webhook_receiver():
#     message_text = []
#     try:
#         # Captura os dados recebidos no webhook
#         data = request.json

#         # Acessa a mensagem de texto recebida
#         message = data.get("text", {}).get("message", "")
#         phone = data.get("phone")

#         # Verifica se o número @5522999920563 está na mensagem
#         if "@5522999920563" in message and "bgp" in message:
#             print("mensagem com bgp ")
#             phone_to_send = phone
#             group_description = get_group_metadata(phone)
#             as_list = extract_as_numbers(group_description)

#             for asn in as_list:
#                 informations = get_bgp_items_by_asn(asn)
#                 message_text.extend(informations)  # Use extend para adicionar itens à lista

#             # Monta uma mensagem organizada
#             if message_text:
#                 formatted_message = "\n".join(message_text)  # Junta as informações em uma única string
#                 text_message = (
#                     f"Tem algo aqui: \n{formatted_message}"  # Aqui você pode customizar a mensagem, se necessário
#                 )
#             else:
#                 text_message = "Nenhuma informação encontrada para os ASNs fornecidos."

#             # Encaminha a mensagem via Z-API
#             message_sender.send_message(phone_to_send, text_message)

#             return (
#                 jsonify(
#                     {"status": "success", "message": "Mensagem encaminhada via Z-API"}
#                 ),
#                 200,
#             )
#         else:
#             return (
#                 jsonify(
#                     {
#                         "status": "ignored",
#                         "message": "Mensagem não contém o número esperado",
#                     }
#                 ),
#                 200,
#             )

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500
