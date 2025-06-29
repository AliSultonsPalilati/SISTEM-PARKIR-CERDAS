from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import ssl
import threading
import os
from collections import deque
import random 

# --- Konfigurasi MQTT ---
ALAMAT_BROKER = "broker.hivemq.com"
PORT_BROKER = 8883
USER_MQTT = "parkir_user" 
PASS_MQTT = "parkir123"  
TOPIK_LANGGANAN = "/parkirCerdas-Alisultn/lantai1/#"

# --- Variabel Global untuk Data ---
status_slot_terbaru = {}
log_aktivitas = deque(maxlen=10) 
data_lock = threading.Lock() 

# --- Konfigurasi Aplikasi Web Flask ---
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Konfigurasi Login untuk Web
monitor_USER = "Alisultn"
monitor_PASS = "admin123"

def saat_terhubung(klien, data_pengguna, bendera, kode_hasil):
    if kode_hasil == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [MONITOR] Terhubung ke Broker MQTT!")
        klien.subscribe(TOPIK_LANGGANAN)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [MONITOR] Gagal terhubung, kode: {kode_hasil}")

def saat_pesan_diterima(klien, data_pengguna, pesan):
    with data_lock:
        try:
            payload_str = pesan.payload.decode('utf-8')
            data = json.loads(payload_str)
            id_slot = data.get('id_slot')
            status_baru = data.get('status')
            
            if id_slot and status_baru:
                # Cek apakah status berubah untuk ditambahkan ke log
                if status_slot_terbaru.get(id_slot) != status_baru:
                    waktu = datetime.now().strftime('%H:%M:%S')
                    log_aktivitas.appendleft(f"[{waktu}] Slot {id_slot} sekarang {status_baru}")

                # Update data slot terbaru
                status_slot_terbaru[id_slot] = status_baru
                
        except (json.JSONDecodeError, AttributeError):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [MQTT-WEB] Pesan tidak valid diterima.")

def jalankan_klien_mqtt():
    # Gunakan client_id yang unik setiap kali dijalankan untuk menghindari masalah koneksi
    klien = mqtt.Client(client_id=f"monitor-web-{random.randint(100,999)}")
    klien.on_connect = saat_terhubung
    klien.on_message = saat_pesan_diterima
    klien.username_pw_set(USER_MQTT, PASS_MQTT)
    klien.tls_set(tls_version=ssl.PROTOCOL_TLS)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [MONITOR] Mencoba terhubung ke {ALAMAT_BROKER}...")
    klien.connect(ALAMAT_BROKER, PORT_BROKER, 60)
    klien.loop_forever()

# --- Rute Aplikasi Web ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == monitor_USER and request.form.get('password') == monitor_PASS:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/data')
def get_monitor_data():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
        
    with data_lock:
        # Hitung statistik
        total_slots = len(status_slot_terbaru)
        terisi = list(status_slot_terbaru.values()).count("TERISI")
        kosong = total_slots - terisi

        data_untuk_api = {
            "slot_status": status_slot_terbaru,
            "summary": {
                "total": total_slots,
                "terisi": terisi,
                "kosong": kosong,
            },
            "log": list(log_aktivitas),
            "waktu_sekarang": datetime.now().strftime('%H:%M:%S')
        }
    return jsonify(data_untuk_api)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Jalankan klien MQTT di thread terpisah
    mqtt_thread = threading.Thread(target=jalankan_klien_mqtt, daemon=True)
    mqtt_thread.start()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] [WEB] Buka monitor di: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)