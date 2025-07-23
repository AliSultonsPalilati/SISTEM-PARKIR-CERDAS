import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime
import ssl

# --- Konfigurasi ---
ALAMAT_BROKER = "broker.hivemq.com"
PORT_BROKER = 8883
USER_MQTT = "Alisultn" 
PASS_MQTT = "parkir123"  

TOPIK_DASAR = "/parkirCerdas-Alisultn/lantai1"

# Daftar slot parkir yang akan disimulasikan
DAFTAR_SLOT_PARKIR = [f"A{i+1}" for i in range(5)] + [f"B{i+1}" for i in range(5)]
status_slot_saat_ini = {slot: "KOSONG" for slot in DAFTAR_SLOT_PARKIR}

def saat_terhubung(klien, data_pengguna, bendera, kode_hasil):
    if kode_hasil == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Terhubung ke Broker!")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Gagal terhubung, kode: {kode_hasil}")

def buat_data_parkir(id_slot):
    global status_slot_saat_ini
    
    # Peluang 30% untuk status berubah setiap siklus
    if random.random() < 0.3:
        status_slot_saat_ini[id_slot] = "TERISI" if status_slot_saat_ini[id_slot] == "KOSONG" else "KOSONG"

    data_yang_dikirim = {
        "id_slot": id_slot,
        "status": status_slot_saat_ini[id_slot],
        "waktu_update": datetime.now().isoformat()
    }
    return data_yang_dikirim

if __name__ == "__main__":
    klien = mqtt.Client(client_id=f"publisher-parkir-{random.randint(100,999)}")
    klien.on_connect = saat_terhubung
    klien.username_pw_set(USER_MQTT, PASS_MQTT)
    klien.tls_set(tls_version=ssl.PROTOCOL_TLS)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Mencoba terhubung ke {ALAMAT_BROKER}...")
    klien.connect(ALAMAT_BROKER, PORT_BROKER, 60)
    klien.loop_start()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Simulasi sensor parkir dimulai.")

    try:
        while True:
            slot_terpilih = random.choice(DAFTAR_SLOT_PARKIR)
            data_parkir = buat_data_parkir(slot_terpilih)
            
            topik_kirim = f"{TOPIK_DASAR}/{slot_terpilih}/status"
            
            payload = json.dumps(data_parkir)
            klien.publish(topik_kirim, payload, qos=1)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] KIRIM ke '{topik_kirim}': {payload}")
            
            time.sleep(random.uniform(1, 3)) # dikirim setiap 1-3 detik
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Simulasi dihentikan.")
    finally:
        klien.loop_stop()
        klien.disconnect()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [PUBLISHER] Koneksi MQTT diputus.")