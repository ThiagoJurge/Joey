from flask import Blueprint, request, jsonify
from models.message_sender import MessageSender
from config import Config
import requests, re


webhook_zapi = Blueprint("webhook_zapi", __name__)
message_sender = MessageSender()


def get_group_metadata(phone):
    """Obtém os metadados de um grupo específico."""
    base_url = Config.NEW_API_URL
    headers = {
        "Client-Token": Config.CLIENT_TOKEN,
        "Content-Type": "application/json",
    }
    url_metadata = f"{base_url}/group-metadata/{phone}"
    response = requests.get(url_metadata, headers=headers).json()
    return response["description"]

def extract_as_numbers(text_list):
    # Regex to match "AS" followed by digits
    pattern = r'AS(\d+)'

    as_numbers = []

    # Loop over each text in the list
    for text in text_list:
        # Find all matches of the pattern in the current text
        matches = re.findall(pattern, text)
        as_numbers.extend(matches)  # Add the found matches to the result list

    return as_numbers



@webhook_zapi.route("//webhook-receiver", methods=["POST"])
def webhook_receiver():
    try:
        # Captura os dados recebidos no webhook
        data = request.json

        # Acessa a mensagem de texto recebida
        message = data.get("text", {}).get("message", "")
        phone = data.get("phone")

        # Verifica se o número @5522999920563 está na mensagem
        if "@5522999920563" in message and "bgp" in message:
            phone_to_send = phone
            group_description = get_group_metadata(phone)
            as_list = extract_as_numbers(group_description)
            text_message = (
                f"{as_list}"  # Aqui você pode customizar a mensagem, se necessário
            )

            # Encaminha a mensagem via Z-API
            message_sender.send_message(phone_to_send, text_message)

            return (
                jsonify(
                    {"status": "success", "message": "Mensagem encaminhada via Z-API"}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "status": "ignored",
                        "message": "Mensagem não contém o número esperado",
                    }
                ),
                200,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
