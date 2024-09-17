from flask import Blueprint, request, jsonify
from scripts.ripe import RipeQuery
from flask_caching import Cache
import hashlib

def create_arc_tools_blueprint(cache: Cache):
    arc_tools = Blueprint("arc_tools", __name__)

    # Função personalizada para gerar a chave de cache baseada no ASN
    def cache_key():
        data = request.json
        asn = data.get("asn")
        return f"arc_tools_{asn}"

    @arc_tools.route("/data/arc_tools", methods=["POST"])
    @cache.cached(timeout=300, key_prefix=cache_key)  # Cache com base no valor do ASN
    def handle_arc_tools():
        data = request.json
        asn = data.get("asn")
        ripe = RipeQuery()
        data = ripe.verify_asn(str(asn))
        return data, 200  # Certifique-se de retornar a resposta como JSON

    return arc_tools
