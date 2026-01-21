# MQTT CO2 Sensor Simulation & Performance Monitor
This repository contains two Python scripts demonstrating a real-time IoT telemetry pipeline using the **MQTT protocol**. It simulates a CO2 sensor sending data from a local machine to a remote server while measuring network latency.
## 🚀 Features
* **CO2 Simulation:** Generates realistic "random walk" CO2 levels (PPM).
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
