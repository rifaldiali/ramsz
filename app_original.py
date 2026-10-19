
import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/notify-demo", methods=["POST"])
def notify_demo():
    if not BOT_TOKEN or not CHAT_ID:
        return {"error": "Konfigurasi Telegram belum lengkap"}, 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": (
                    "Demonstrasi akademis GetlocRams\n"
                    "Notifikasi pengujian berhasil.\n"
                    "Pesan ini tidak memuat lokasi perangkat."
                )
            },
            timeout=10
        )
        response.raise_for_status()

        if not response.json().get("ok"):
            return {"error": "Telegram menolak pesan"}, 502

        return {"status": "Notifikasi terkirim"}

    except requests.RequestException:
        app.logger.exception("Gagal mengirim notifikasi")
        return {"error": "Notifikasi gagal dikirim"}, 502


@app.route("/test-location-demo", methods=["POST"])
def test_location_demo():
    # Data sintetis untuk menguji integrasi, bukan lokasi perangkat.
    test_data = {
        "latitude": -6.200000,
        "longitude": 106.816666,
        "accuracy": 100,
        "note": "KOORDINAT SINTETIS - BUKAN LOKASI NYATA"
    }

    if not BOT_TOKEN or not CHAT_ID:
        return {"error": "Konfigurasi Telegram belum lengkap"}, 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": (
                    "TES INTEGRASI GEOLOKASI\n"
                    f"Latitude: {test_data['latitude']}\n"
                    f"Longitude: {test_data['longitude']}\n"
                    f"Akurasi contoh: ±{test_data['accuracy']} meter\n"
                    f"Status: {test_data['note']}"
                )
            },
            timeout=15
        )
        response.raise_for_status()

        if not response.json().get("ok"):
            return {"error": "Telegram menolak pesan"}, 502

        return {"status": "Tes berhasil", "data": test_data}

    except requests.RequestException:
        app.logger.exception("Tes integrasi Telegram gagal")
        return {"error": "Pengiriman tes gagal"}, 502

if __name__ == "__main__":
    app.run(debug=True, port=5001)

