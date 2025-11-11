# Nama File: api_service.py
# Versi Lengkap dan Sudah Diperbaiki
# Service untuk mengambil data dari OpenWeatherMap dan Wilayah.id API

import requests
import os

# === KONFIGURASI API OPENWEATHERMAP ===
# REKOMENDASI: Pindahkan API key ke environment variable atau file .env
API_KEY = os.getenv("OPENWEATHER_API_KEY", "375e722d3184ce77b16ae59068ef9480")
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather?"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?"

# === KONFIGURASI API WILAYAH.ID ===
API_WILAYAH_BASE_URL = "https://wilayah.id/api"


# ========================================
# FUNGSI UNTUK CUACA SAAT INI
# ========================================

def get_current_weather(city_name):
    """
    Mengambil data cuaca SAAT INI dari OpenWeatherMap.
    
    Parameters:
        city_name (str): Nama kota yang ingin dicari
        
    Returns:
        dict: Dictionary berisi data cuaca atau error message
    """
    complete_url = BASE_URL_CURRENT + "appid=" + API_KEY + "&q=" + city_name + "&units=metric"
    
    try:
        response = requests.get(complete_url, timeout=5)
        response.raise_for_status()  # Raise exception untuk status 4xx/5xx
        data = response.json()

        # Cek kode internal dari OpenWeatherMap
        if data.get("cod") != 200: 
            return {"error": data.get("message", "Kota tidak ditemukan!")}

        # Proses data mentah menjadi dictionary yang bersih
        main_data = data["main"]
        weather_description = data["weather"][0]["description"].lower()
        
        return {
            "city": data["name"],  # Gunakan nama dari API untuk konsistensi
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "pressure": main_data["pressure"],
            "description": weather_description.title(),  # Contoh: "Clear Sky"
            "raw_description": weather_description,      # Contoh: "clear sky"
            "wind_speed": data["wind"]["speed"],
            "feels_like": main_data.get("feels_like", main_data["temp"]),
            "temp_min": main_data.get("temp_min", main_data["temp"]),
            "temp_max": main_data.get("temp_max", main_data["temp"])
        }
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Kota tidak ditemukan. Periksa ejaan nama kota."}
        return {"error": f"Error HTTP: {e.response.status_code}"}
        
    except requests.exceptions.ConnectionError:
        return {"error": "Error koneksi. Periksa koneksi internet Anda."}
        
    except requests.exceptions.Timeout:
        return {"error": "Permintaan ke server timeout. Coba lagi."}
        
    except KeyError as e:
        return {"error": f"Data tidak lengkap dari API: {e}"}
        
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}"}


# ========================================
# FUNGSI UNTUK RAMALAN 5 HARI
# ========================================

def get_5day_forecast(city_name):
    """
    Mengambil data RAMALAN 5 HARI dari OpenWeatherMap.
    
    Parameters:
        city_name (str): Nama kota yang ingin dicari
        
    Returns:
        list atau dict: List berisi ramalan 5 hari, atau dict dengan error
    """
    complete_url = BASE_URL_FORECAST + "appid=" + API_KEY + "&q=" + city_name + "&units=metric"
    
    try:
        response = requests.get(complete_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # API ini mengembalikan string "200" untuk sukses
        if data.get("cod") != "200":
            return {"error": data.get("message", "Kota tidak ditemukan")}

        forecast_list = data.get('list', [])
        processed_forecast = []
        seen_days = set()  # Untuk melacak hari yang sudah ditambahkan

        # Loop melalui semua data ramalan (biasanya per 3 jam)
        for item in forecast_list:
            timestamp = item.get('dt_txt', '')
            if not timestamp:
                continue
                
            day = timestamp.split(" ")[0]  # Ambil bagian tanggalnya (YYYY-MM-DD)
            
            # Hanya ambil satu data per hari (data pertama dari hari itu)
            if day not in seen_days:
                seen_days.add(day)
                
                raw_desc = item['weather'][0]['description'].lower()
                processed_forecast.append({
                    "day": day,
                    "temp": item['main']['temp'],
                    "description": raw_desc.title(),  # Contoh: "Clear Sky"
                    "raw_description": raw_desc,      # Contoh: "clear sky"
                    "humidity": item['main']['humidity'],
                    "temp_min": item['main'].get('temp_min', item['main']['temp']),
                    "temp_max": item['main'].get('temp_max', item['main']['temp'])
                })
                
                # Batasi hanya 5 hari
                if len(processed_forecast) >= 5:
                    break
        
        return processed_forecast  # Mengembalikan list of dictionaries
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Kota tidak ditemukan. Periksa ejaan nama kota."}
        return {"error": f"Error HTTP: {e.response.status_code}"}
        
    except requests.exceptions.ConnectionError:
        return {"error": "Error koneksi. Periksa koneksi internet Anda."}
        
    except requests.exceptions.Timeout:
        return {"error": "Permintaan ke server timeout. Coba lagi."}
        
    except KeyError as e:
        return {"error": f"Data tidak lengkap dari API: {e}"}
        
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}"}


# ========================================
# FUNGSI PROXY UNTUK WILAYAH.ID API
# ========================================

def get_wilayah_data(endpoint):
    """
    Fungsi 'proxy' untuk mengambil data dari wilayah.id API.
    
    Parameters:
        endpoint (str): Bagian setelah /api/ 
                       Contoh: "/provinces.json" atau "/regencies/31.json"
    
    Returns:
        tuple: (data, status_code)
               - data: Dictionary berisi response JSON atau error message
               - status_code: HTTP status code (200, 404, 500, dll)
    """
    url = f"{API_WILAYAH_BASE_URL}{endpoint}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Error jika status 4xx/5xx
        
        # PERBAIKAN: Kembalikan 2 nilai (data, status_code)
        return response.json(), 200
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error {e.response.status_code}"
        print(f"Error saat mengambil data wilayah dari {url}: {error_msg}")
        
        # Kembalikan 2 nilai
        return {"error": error_msg}, e.response.status_code
        
    except requests.exceptions.ConnectionError:
        error_msg = "Error koneksi ke server wilayah.id"
        print(f"Error koneksi: {error_msg}")
        return {"error": error_msg}, 503
        
    except requests.exceptions.Timeout:
        error_msg = "Request timeout ke server wilayah.id"
        print(f"Timeout: {error_msg}")
        return {"error": error_msg}, 504
        
    except Exception as e:
        error_msg = f"Terjadi kesalahan: {str(e)}"
        print(f"Error umum saat mengambil data wilayah: {error_msg}")
        return {"error": error_msg}, 500


# ========================================
# FUNGSI HELPER (OPSIONAL)
# ========================================

def validate_api_key():
    """
    Memvalidasi apakah API key OpenWeatherMap valid.
    
    Returns:
        tuple: (is_valid, message)
    """
    test_url = BASE_URL_CURRENT + "appid=" + API_KEY + "&q=London&units=metric"
    
    try:
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            return True, "API key valid"
        elif response.status_code == 401:
            return False, "API key tidak valid"
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, f"Tidak dapat memvalidasi API key: {str(e)}"


def get_weather_by_coordinates(lat, lon):
    """
    Mengambil cuaca berdasarkan koordinat latitude dan longitude.
    
    Parameters:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        dict: Data cuaca atau error message
    """
    url = f"{BASE_URL_CURRENT}appid={API_KEY}&lat={lat}&lon={lon}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("cod") != 200:
            return {"error": data.get("message", "Koordinat tidak valid")}
            
        main_data = data["main"]
        weather_description = data["weather"][0]["description"].lower()
        
        return {
            "city": data["name"],
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "pressure": main_data["pressure"],
            "description": weather_description.title(),
            "raw_description": weather_description,
            "wind_speed": data["wind"]["speed"]
        }
        
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}"}


# ========================================
# TESTING (Jika dijalankan langsung)
# ========================================

if __name__ == "__main__":
    print("=== Testing API Service ===\n")
    
    # Test 1: Validasi API Key
    print("1. Validasi API Key:")
    is_valid, message = validate_api_key()
    print(f"   {message}\n")
    
    if is_valid:
        # Test 2: Cuaca Saat Ini
        print("2. Test Cuaca Saat Ini (Jakarta):")
        weather = get_current_weather("Jakarta")
        if "error" in weather:
            print(f"   ❌ Error: {weather['error']}")
        else:
            print(f"   ✅ Kota: {weather['city']}")
            print(f"   🌡️  Suhu: {weather['temperature']}°C")
            print(f"   📝 Kondisi: {weather['description']}\n")
        
        # Test 3: Ramalan 5 Hari
        print("3. Test Ramalan 5 Hari (Jakarta):")
        forecast = get_5day_forecast("Jakarta")
        if isinstance(forecast, dict) and "error" in forecast:
            print(f"   ❌ Error: {forecast['error']}")
        else:
            print(f"   ✅ Berhasil mendapat {len(forecast)} hari ramalan")
            for day in forecast[:2]:  # Tampilkan 2 hari pertama
                print(f"   📅 {day['day']}: {day['temp']}°C - {day['description']}")
        print()
        
        # Test 4: Wilayah.id API
        print("4. Test Wilayah.id API (Provinsi):")
        provinces, status = get_wilayah_data("/provinces.json")
        if status == 200:
            print(f"   ✅ Berhasil mendapat {len(provinces.get('data', []))} provinsi")
        else:
            print(f"   ❌ Error: {provinces.get('error', 'Unknown error')}")
    
    print("\n=== Testing Selesai ===")