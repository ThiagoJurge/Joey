from apscheduler.schedulers.background import BackgroundScheduler
import atexit, requests
from models.message_sender import MessageSender
from config import Config

scheduler = BackgroundScheduler()
scheduler.start()

def send_scheduled_message():
    print("Sending message")
    response = requests.get('http://187.16.255.94:4321/api/interrupcoes').json()
    message_sender = MessageSender(Config.API_URL)
    message_sender.send_message("5522997359668-1524147176", f"{response['interrupcoes'][0]}\n\n{response['interrupcoes'][1]}")

atexit.register(lambda: scheduler.shutdown())
