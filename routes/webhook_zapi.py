from flask import Blueprint, request, jsonify
from models.message_sender import MessageSender

webhook_zapi = Blueprint("webhook_zapi", __name__)
message_sender = MessageSender()


@webhook_zapi.route("//webhook-receiver", methods=["POST"])
def webhook_receiver():
    try:
        # Captura os dados recebidos no webhook
        data = request.json

        # Acessa a mensagem de texto recebida
        message = data.get('text', {}).get('message', '')
        phone = data.get('phone')

        # Verifica se o número @5522999920563 está na mensagem
        if '@5522999920563' in message:
            phone_to_send = phone
            text_message = message  # Aqui você pode customizar a mensagem, se necessário

            # Encaminha a mensagem via Z-API
            message_sender.send_message(phone_to_send, text_message)

            return jsonify({"status": "success", "message": "Mensagem encaminhada via Z-API"}), 200
        else:
            return jsonify({"status": "ignored", "message": "Mensagem não contém o número esperado"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
