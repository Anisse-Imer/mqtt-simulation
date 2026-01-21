# MQTT CO2 Sensor Simulation & Performance Monitor
This repository contains two Python scripts demonstrating a real-time IoT telemetry pipeline using the **MQTT protocol**. It simulates a CO2 sensor sending data from a local machine to a remote server while measuring network latency.
## 🚀 Features
* **CO2 Simulation:** Generates realistic "random walk" CO2 levels (PPM).
* **CO2 Alerts:** Depending on the scale of the CO2 levels, we have different kind of alerts.
* **CO2 Graphics** Generates a real time graphic of the CO2 level, for every 20 results.
* **Performance Tracking:** Calculates end-to-end latency in milliseconds ().
* **JSON Packaging:** Demonstrates how to structure IoT payloads.
* **Asynchronous:** Uses the `paho-mqtt` Version 2.0 API.
## 🛠 Prerequisites
* Python 3.10+
* An MQTT Broker (Default: `broker.hivemq.com`)
Install the required library:
```bash
pip install paho-mqtt
```
## 📂 Project Structure
* `publisher.py`: The "Local Machine" script. Simulates a CO2 captor and pushes data.
* `subscriber.py`: The "Server" script. Listens for data and calculates the time-of-flight.
## 🚦 How to Run
### 1. Start the Monitor (Server)
Run this on your Ubuntu server first so it's ready to catch the data:
```bash
python3 subscriber.py
```
### 2. Start the Captor (Local Machine)
Run this on your local machine to begin transmitting:
```bash
python3 publisher.py
```
## 📊 Performance Overview
The system measures latency using the following logic:
1. **Publisher** attaches a high-precision timestamp to the JSON payload.
2. **Subscriber** subtracts that timestamp from the current time upon arrival.
| Metric | Description |
| --- | --- |
| **Payload Size** | ~80 Bytes |
| **Frequency** | 1 Message/Second (Adjustable) |
| **Average Latency** | Dependent on Broker location (typically 30ms - 150ms) |
---

## 🔒 Security & Configuration
This project follows **ETSI EN 303 645** IoT security standards by isolating credentials from the source code.
### ⚙️ Setup (.env)
Create a `.env` file in the root directory. **Never commit this file to GitHub.**
```text
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
SUBSCRIBER_ID=sub-heztner-01
SUBSCRIBER_TOKEN=secret_token_sub
PUBLISHER_ID=pub-sensor-01
PUBLISHER_TOKEN=secret_token_pub
```
### 🛡️ Security Logic
* **Authentication:** Uses `username_pw_set()` to prevent unauthorized broker access.
* **Unique Identity:** Distinct `CLIENT_ID` per device avoids session hijacking and enables audit logs.
* **Decoupling:** `python-dotenv` ensures tokens stay local and are never exposed in the code.
* **Reliability:** **QoS 1** is enforced to guarantee delivery of critical CO2 data despite network instability.
