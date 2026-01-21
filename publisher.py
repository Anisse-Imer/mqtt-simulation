import paho.mqtt.client as mqtt
import time
import json
import random

# Use Version 2.0 API
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883, 60)

co2_level = 420.0  # Starting baseline (Outdoor air is ~400-450)

print("CO2 Sensor Simulation Started...")

try:
    while True:
        # Simulate a realistic fluctuation (+/- 2 PPM)
        co2_level += random.uniform(-2, 2)
        
        # Prepare the data packet
        data = {
            "co2": round(co2_level, 2),
            "unit": "PPM",
            "timestamp": time.time()  # For performance tracking
        }
        
        payload = json.dumps(data)
        client.publish("sensors/room1/co2", payload)
        
        print(f"Sent: {data['co2']} PPM")
        time.sleep(1) 
except KeyboardInterrupt:
    client.disconnect()
    