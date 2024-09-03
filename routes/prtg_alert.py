from flask import Blueprint, request, jsonify
from models.ZApiGroupExtractor import ZApiGroupExtractor
from models.message_sender import MessageSender
from models.alarm_handler import AlarmHandler
from config import Config

prtg_alert = Blueprint("prtg", __name__)

ZApiGroupExtractor = ZApiGroupExtractor()
message_sender = MessageSender(Config.API_URL)
alarm_handler = AlarmHandler(ZApiGroupExtractor, message_sender)


@prtg_alert.route("/send_message", methods=["POST"])
def send_message():
    message_text = request.form
    itens = []
    for item in message_text:
        itens.append(item)

    response = alarm_handler.process_message(itens[0])
    return jsonify(response)
