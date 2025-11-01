import requests 

API_KEY = "375e722d3184ce77b16ae59068ef9480"
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

def get_5day_forecast(city_name):
    """Mengambil data RAMALAN 5 HARI dari OpenWeatherMap."""
    complete_url = BASE_URL_FORECAST + "appid=" + API_KEY + "&q=" + city_name + "&units=metric"
    
    try:
        response = requests.get(complete_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != "200": # API ini mengembalikan string "200"
            return {"error": data.get("message", "Kota tidak ditemukan")}

        forecast_list = data.get('list', [])
        processed_forecast = []
        seen_days = set() # Untuk melacak hari yang sudah ditambahkan

        # Loop melalui semua data ramalan (biasanya per 3 jam)
        for item in forecast_list:
            timestamp = item.get('dt_txt', '')
            day = timestamp.split(" ")[0] # Ambil bagian tanggalnya (YYYY-MM-DD)
            
            # Hanya ambil satu data per hari
            if day not in seen_days:
                seen_days.add(day)
                
                # --- INI BAGIAN YANG DIPERBARUI ---
                raw_desc = item['weather'][0]['description'].lower()
                processed_forecast.append({
                    "day": day,
                    "temp": item['main']['temp'],
                    "description": raw_desc.title(), # e.g., "Clear Sky"
                    "raw_description": raw_desc      # e.g., "clear sky"
                })
                # --- AKHIR BAGIAN YANG DIPERBARUI ---
                
                # Batasi hanya 5 hari
                if len(processed_forecast) >= 5:
                    break
        
        return processed_forecast # Mengembalikan list of dictionaries
        
    # --- BLOK INI YANG MUNGKIN ANDA LUPAKAN ---
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Kota tidak ditemukan."}
        return {"error": f"Error HTTP: {e.response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Error koneksi."}
    except requests.exceptions.Timeout:
        return {"error": "Permintaan timeout."}
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {e}"}