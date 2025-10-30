# Nama File: api_service.py
# (VERSI YANG SUDAH DIPERBARUI UNTUK IKON RAMALAN)

import requests

API_KEY = "Kosong"
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather?"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?"

def get_current_weather(city_name):
    """Mengambil data cuaca SAAT INI dari OpenWeatherMap."""
    complete_url = BASE_URL_CURRENT + "appid=" + API_KEY + "&q=" + city_name + "&units=metric"

    try:
        response = requests.get(complete_url, timeout=5) # Tambahkan timeout 5 detik
        response.raise_for_status() # Akan error jika status 4xx atau 5xx
        data = response.json()

        # Cek kode internal dari OpenWeatherMap
        if data.get("cod") != 200: 
            return {"error": data.get("message", "Kota tidak ditemukan!")}

        # Proses data mentah menjadi dictionary yang bersih
        main_data = data["main"]
        weather_description = data["weather"][0]["description"].lower()
        
        return {
            "city": data["name"], # Gunakan nama dari API untuk konsistensi
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "pressure": main_data["pressure"],
            "description": weather_description.title(), # Misal: "Clear Sky"
            "raw_description": weather_description,     # Misal: "clear sky"
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Kota tidak ditemukan."}
        return {"error": f"Error HTTP: {e.response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Error koneksi. Periksa internet Anda."}
    except requests.exceptions.Timeout:
        return {"error": "Permintaan ke server timeout."}
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {e}"}

#---Lanjutkan----#