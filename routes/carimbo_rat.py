from flask import Blueprint, request, jsonify, render_template
from models.message_sender import MessageSender
from config import Config
from datetime import datetime
import requests
import json
import os

carimbo_rat_bp = Blueprint("carimbo_rat", __name__)

message_sender = MessageSender(Config.API_URL)


def save_form_data(data, filename="form_data.json"):
    # Adicionar a data e hora ao dado
    data_with_metadata = {
        "timestamp": datetime.now().isoformat(),  # Adiciona a data e hora atual
        "used": False,  # Adiciona o índice 'used' com valor 'false'
        "data": data,  # Adiciona os dados do formulário
    }

    # Verifica se o arquivo existe e não está vazio
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                all_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            all_data = []
    else:
        all_data = []

    all_data.append(data_with_metadata)

    with open(filename, "w") as file:
        json.dump(all_data, file, indent=4)


# Listas de opções válidas
VALID_EQUIPES = [
    "Equipe Infraestrutura 01",
    "Equipe Infraestrutura 02",
    "Equipe Operacional Angra",
    "Equipe Operacional Campos",
    "Equipe Operacional Lagos 01",
    "Equipe Operacional Lagos 02",
    "Equipe Operacional Linhares",
    "Equipe Operacional NOF-01",
    "Equipe Operacional NOF-02",
    "Equipe Operacional NOF-03",
    "Equipe Operacional Paraty",
    "Equipe Operacional Petrópolis",
    "Equipe Operacional RIO-01",
    "Equipe Operacional RIO-02",
    "Equipe Operacional Vitória",
    "Equipe Operacional Volta Redonda",
]

VALID_ATIVIDADES = [
    "Ações Preventivas",
    "Adequação Companhia Energia",
    "Ativar Backbone",
    "Ativar Cliente",
    "Atividades Administrativas",
    "Atividades Para Ampliação de Backbone",
    "Coletar Curvas",
    "Conjunta",
    "Consertos ou Logística de veículos",
    "Formatação de fibras",
    "Logística de Materiais",
    "Manutenção/Verificação de Infraestrutura Site",
    "Monitoramento com OTDR",
    "Testes de RFC",
    "Verificar Atenuações",
    "Verificar Equipamentos (módulos, switchs, cordões e etc)",
    "Verificar Rompimento",
    "Vistoria",
]


@carimbo_rat_bp.route("/carimbo_rat", methods=["GET"])
def carimbo_rat():
    return render_template("carimbo_rat.html")


@carimbo_rat_bp.route("/send_carimbo_rat", methods=["POST"])
def submit_form():
    if request.content_type != "application/json":
        return jsonify({"message": "Content-Type must be application/json"}), 415

    form_data = {
        "entry_825154660": request.json.get("entry_825154660", ""),
        "entry_387529666": request.json.get("entry_387529666", ""),
        "entry_1071483611": request.json.get("entry_1071483611", ""),
        "entry_2130349081": request.json.get("entry_2130349081", ""),
        "entry_1932602901": request.json.get("entry_1932602901", ""),
        "entry_313095559": request.json.get("entry_313095559", ""),
        "entry_1202092668": request.json.get("entry_1202092668", ""),
    }

    # Validações
    errors = []

    # ID deve ser um número inteiro
    try:
        int(form_data["entry_825154660"])
    except ValueError:
        errors.append("ID deve ser um número inteiro.")

    # Equipe deve ser uma das opções válidas
    if form_data["entry_387529666"] not in VALID_EQUIPES:
        errors.append("Equipe inválida.")

    # Atividade deve ser uma das opções válidas
    if form_data["entry_313095559"] not in VALID_ATIVIDADES:
        print(form_data["entry_313095559"])
        errors.append("Atividade inválida.")

    # Se houver erros, retorna a mensagem de erro
    if errors:
        return jsonify({"message": "Erros de validação", "errors": errors}), 400

    # Se não houver erros, envia o formulário
    message = f"""`ACIONAMENTO RAT`
Protocolo: {form_data['entry_825154660']}
Equipe: {form_data['entry_387529666']}
Cliente(s): {form_data['entry_1202092668']}"""

    # Envia a mensagem formatada
    # message_sender.send_message("120363303090993469", message)
    save_form_data(form_data)
    return jsonify({"message": "Formulário enviado com sucesso!"}), 200

    # carimbo_rat = CarimboRat()
    # url = carimbo_rat.get_form_url(form_data)

    # response = requests.get(url)

    # if response.status_code == 200:
    #     return jsonify({"message": "Formulário enviado com sucesso!"}), 200
    # else:
    #     return (
    #         jsonify(
    #             {"message": f"Erro ao enviar o formulário: {response.status_code}"}
    #         ),
    #         response.status_code,
    #     )
