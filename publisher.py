import paho.mqtt.client as mqtt
import time
import json
import random
import os
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()

# Configuration ETSI: Utilisation d'identifiants uniques
CLIENT_ID = os.getenv("PUBLISHER_ID")
TOKEN = os.getenv("PUBLISHER_TOKEN")
BROKER = os.getenv("MQTT_BROKER")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
client.username_pw_set(CLIENT_ID, TOKEN) # Authentification sécurisée

client.connect(BROKER, int(os.getenv("MQTT_PORT")), 60)

co2_level = 420.0
trend = 1.0 

print(f"Simulation ETSI lancée (ID: {CLIENT_ID})")

try:
    while True:
        co2_level += random.uniform(20, 100) * trend
        
        data = {
            "device_id": CLIENT_ID,
            "co2": round(co2_level, 2),
            "timestamp": time.time(),
            "status": "normal" if co2_level < 1000 else "alert"
        }
        
        # Publication avec QoS 1 pour respect de la norme de fiabilité
        client.publish("sensors/room1/co2", json.dumps(data), qos=1)
        print(f"Envoyé: {data['co2']} PPM")
        
        if co2_level > 10000: break 
        time.sleep(0.5) 
        
except KeyboardInterrupt:
    client.disconnect()
    