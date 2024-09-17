from flask import Flask
from routes.prtg_alert import prtg_alert
from routes.webhook_zapi import webhook_zapi
from routes.arc_tools import create_arc_tools_blueprint
from flask_caching import Cache
import threading

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# Criando o blueprint com o cache
arc_tools = create_arc_tools_blueprint(cache)

app.register_blueprint(prtg_alert)
app.register_blueprint(webhook_zapi)
app.register_blueprint(arc_tools)

@app.errorhandler(405)
def method_not_allowed(e):
    return e, 405

@app.errorhandler(404)
def not_found(e):
    return e, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
