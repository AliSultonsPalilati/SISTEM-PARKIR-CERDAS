import paho.mqtt.client as mqtt
import json
from datetime import datetime
import ssl
import random 

# --- Konfigurasi ---
ALAMAT_BROKER = "broker.hivemq.com"
PORT_BROKER = 8883
TOPIK_LANGGANAN = "/parkirCerdas-Alisultn/lantai1/#"

def saat_terhubung(klien, data_pengguna, bendera, kode_hasil):
    if kode_hasil == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [SUBSCRIBER] Terhubung ke Broker!")
        klien.subscribe(TOPIK_LANGGANAN)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [SUBSCRIBER] Berlangganan ke topik: '{TOPIK_LANGGANAN}'")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [SUBSCRIBER] Gagal terhubung, kode: {kode_hasil}")

def saat_pesan_diterima(klien, data_pengguna, pesan):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Pesan dari '{pesan.topic}':")
    try:
        data = json.loads(pesan.payload.decode('utf-8'))
        print(f"  -> ID Slot: {data.get('id_slot', 'N/A')}, Status: {data.get('status', 'N/A')}")
    except json.JSONDecodeError:
        print(f"  -> ERROR: Payload bukan JSON. Data: {pesan.payload.decode('utf-8')}")

if __name__ == "__main__":
    klien = mqtt.Client(client_id=f"subscriber-debug-{random.randint(100,999)}")
    klien.on_connect = saat_terhubung
    klien.on_message = saat_pesan_diterima

    user_mqtt = input("Masukkan Username MQTT Anda: ")
    pass_mqtt = input("Masukkan Password MQTT Anda: ")
    klien.username_pw_set(user_mqtt, pass_mqtt)
    klien.tls_set(tls_version=ssl.PROTOCOL_TLS)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] [SUBSCRIBER] Mencoba terhubung ke {ALAMAT_BROKER}...")
    klien.connect(ALAMAT_BROKER, PORT_BROKER, 60)
    klien.loop_forever()