import sys
import threading
from app import app as application
from scripts.db_listener import DatabaseMonitor, db_config

# Adicione o diretório do projeto ao sys.path se necessário
sys.path.insert(0, "/home/gabrielm/Lenny")

def start_db_monitor():
    monitor = DatabaseMonitor(db_config)
    monitor.monitor_changes(interval=60)

# Inicia o monitoramento do banco de dados em um thread separado
db_monitor_thread = threading.Thread(target=start_db_monitor)
db_monitor_thread.daemon = True  # Permite que o thread seja encerrado quando o main thread finalizar
db_monitor_thread.start()
