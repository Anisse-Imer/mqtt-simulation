import hashlib
import paho.mqtt.client as mqtt
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SUBSCRIBER_ID")
TOKEN = os.getenv("SUBSCRIBER_TOKEN")
BROKER = os.getenv("MQTT_BROKER")

BLOCKCHAIN:list[dict] = []

def on_message(client, userdata, msg):
    try:
        # 1. Decode payload for processing
        raw_payload = msg.payload  # This is already bytes
        data = json.loads(raw_payload.decode())
        co2 = data['co2']
        
        # Performance/Status Logic
        latency = (time.time() - data['timestamp']) * 1000
        status = "OK"
        if co2 > 1000: status = "AÉRER"
        if co2 > 5000: status = "DANGER"
        print(f"[{status}] ID: {data['device_id']} | CO2: {co2} PPM | Latence: {latency:.2f}ms")

        # 2. Blockchain Logic (The Fix)
        prev_hash = BLOCKCHAIN[-1]["data_hash"] if BLOCKCHAIN else "GENESIS"
        
        # We combine the new data with the previous hash to create the link
        block_string = f"{raw_payload.decode()}{prev_hash}{time.time()}"
        current_hash = hashlib.sha256(block_string.encode()).hexdigest()

        block: dict = {
            "data_hash": current_hash, # This is the unique ID for THIS block
            "prev_hash": prev_hash,
            "timestamp": int(time.time()),
            "value": co2
        }

        BLOCKCHAIN.append(block)
        print(BLOCKCHAIN)
    except Exception as e:
        print(f"Erreur: {e}")

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
    