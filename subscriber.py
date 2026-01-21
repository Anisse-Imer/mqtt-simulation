import paho.mqtt.client as mqtt
import json
import time

def on_message(client, userdata, msg):
    try:
        # Decode the JSON payload
        data = json.loads(msg.payload.decode())
        
        # Calculate performance (latency)
        latency = (time.time() - data['timestamp']) * 1000
        
        print(f"Captured CO2: {data['co2']} PPM | Latency: {latency:.2f}ms")
        
        # Alert logic (Simple performance/safety check)
        if data['co2'] > 1000:
            print("--- WARNING: HIGH CO2 LEVELS DETECTED ---")
            
    except Exception as e:
        print(f"Error decoding message: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("sensors/room1/co2")

print("Server listening for CO2 data...")
client.loop_forever()
