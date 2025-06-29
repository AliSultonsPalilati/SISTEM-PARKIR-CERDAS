# 🚗 Sistem Parkir Cerdas dan Aman Berbasis MQTT

Sistem ini dirancang untuk memantau status slot parkir secara **real-time** menggunakan teknologi **Internet of Things (IoT)** dan protokol komunikasi ringan **MQTT**. Fokus utama sistem adalah menyediakan **informasi parkir yang efisien, cepat, dan aman** kepada pengguna melalui dashboard berbasis web.

---

## 📌 Latar Belakang

Kemacetan lalu lintas di kota besar semakin parah akibat sulitnya mencari tempat parkir. Pengendara kerap membuang waktu berputar-putar, yang berakibat:

- 🚦 Kemacetan meningkat
- 💨 Emisi kendaraan bertambah
- ⏳ Waktu terbuang sia-sia
- 💸 Pendapatan pengelola parkir menurun

Solusi yang ditawarkan adalah sistem parkir pintar berbasis **MQTT dan IoT** yang dapat memantau slot parkir secara **real-time**, meski data yang digunakan masih dalam bentuk simulasi (dummy).

Sistem ini juga dirancang dengan **keamanan berlapis**, memastikan komunikasi antar perangkat tetap aman dan terenkripsi.

---

## ❓ Rumusan Masalah

1. Bagaimana merancang sistem monitoring parkir yang memberikan informasi **ketersediaan slot secara real-time**?
2. Bagaimana mengimplementasikan protokol **MQTT** untuk komunikasi data yang efisien antara **sensor dan dashboard**?

---

## 🎯 Tujuan Proyek

1. **Membangun Prototipe Sistem Parkir Cerdas**  
   Sistem dapat mendeteksi status slot parkir (terisi/kosong) dan menampilkannya secara **real-time** di dashboard.

2. **Menggunakan Protokol MQTT**  
   MQTT digunakan sebagai protokol utama karena sifatnya ringan, cepat, dan cocok untuk IoT.

3. **Menjamin Keamanan Komunikasi**  
   Sistem menerapkan:
   - 🔐 TLS/SSL untuk enkripsi data
   - ✅ Autentikasi klien menggunakan username & password
   - 🛡️ Validasi data untuk menjamin integritas informasi

---

## 🧠 Teknologi yang Digunakan

| Teknologi | Keterangan |
|-----------|------------|
| MQTT      | Protokol komunikasi IoT |
| TLS/SSL   | Enkripsi data saat transmisi |
| Wireshark | Analisis performa komunikasi |
| Web Dashboard | Antarmuka pengguna untuk monitoring |
| Paho MQTT | Library MQTT (Python/JavaScript) |

---

## 🧪 Simulasi dan Pengujian

Sistem diuji menggunakan data simulasi dan **Wireshark** untuk menganalisis:

- ⏱️ **Latensi** dan **Throughput**
- 📦 Efisiensi pengiriman paket
- 📶 Penggunaan bandwidth
- 🔐 Keandalan dan keamanan komunikasi MQTT

---

## 📈 Manfaat Sistem

- ⛔ Mengurangi kemacetan
- 🌱 Menurunkan emisi kendaraan
- 🕒 Meningkatkan efisiensi waktu pengendara
- 💰 Meningkatkan pemanfaatan area parkir
- 🔒 Menjaga keamanan dan kerahasiaan data

---

## 💡 Catatan

- Sistem ini masih berbasis **simulasi (data dummy)** namun dapat dikembangkan untuk diintegrasikan langsung dengan sensor ultrasonik, kamera, atau RFID.
- Penggunaan **broker MQTT publik** (seperti `broker.hivemq.com`) dapat diganti dengan broker privat untuk keperluan skala besar dan keamanan tambahan.

---

## 📂 Struktur Proyek (Contoh)

