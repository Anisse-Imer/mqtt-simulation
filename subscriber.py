import paho.mqtt.client as mqtt
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SUBSCRIBER_ID")
TOKEN = os.getenv("SUBSCRIBER_TOKEN")
BROKER = os.getenv("MQTT_BROKER")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        co2 = data['co2']
        
        # Calcul de la latence (Performance)
        latency = (time.time() - data['timestamp']) * 1000
        
        # Logique d'alerte conforme aux seuils de sécurité
        status = "OK"
        if co2 > 1000: status = "AÉRER"
        if co2 > 5000: status = "DANGER"

        print(f"[{status}] ID: {data['device_id']} | CO2: {co2} PPM | Latence: {latency:.2f}ms")
            
    except Exception as e:
        print(f"Erreur de parsing: {e}")

# Initialisation conforme ETSI : Session persistante (clean_session=False)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
client.username_pw_set(CLIENT_ID, TOKEN)
client.on_message = on_message

client.connect(BROKER, int(os.getenv("MQTT_PORT")), 60)
client.subscribe("sensors/room1/co2", qos=1)

print(f"Serveur Monitoring actif (ID: {CLIENT_ID})...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Arrêt du serveur.")
    