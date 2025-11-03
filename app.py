from flask import Flask, jsonify, request, send_from_directory
import api_service
import data_manager
import os

# Import Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("WARNING: google-generativeai tidak terinstall. Chatbot tidak akan berfungsi.")

app = Flask(__name__, static_folder='frontend', static_url_path='')

# === KONFIGURASI GEMINI AI ===
chat_session = None  # Inisialisasi global variable

if GEMINI_AVAILABLE:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB2avMTSoMnIS8CNmWgSfklANyMAeYl3bI")
    genai.configure(api_key=GEMINI_API_KEY)

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    # Gunakan model terbaru yang tersedia
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",  # Model terbaru dan stabil
        generation_config=generation_config
    )

    SYSTEM_PROMPT = """Kamu adalah asisten cuaca yang ramah dan informatif. 
Tugasmu HANYA menjawab pertanyaan seputar:
- Cuaca (suhu, hujan, angin, kelembaban, dll)
- Fenomena cuaca (tornado, topan, badai, salju, dll)
- Tips dan saran terkait cuaca (pakaian, aktivitas, dll)
- Fakta unik tentang cuaca dan iklim
- Perubahan iklim dan dampaknya

PENTING:
1. Jika ditanya di luar topik cuaca, jawab: "Maaf, saya hanya bisa membantu pertanyaan seputar cuaca."
2. Berikan jawaban singkat dan jelas (maksimal 3-4 paragraf)
3. Gunakan emoji cuaca yang relevan
4. Berikan saran praktis jika perlu

Selalu ramah dan helpful!"""

    chat_session = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Baik, saya siap membantu pertanyaan seputar cuaca!"]}
    ])

# === ROUTE FRONTEND ===

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('frontend', path)
    except:
        return jsonify({"error": "File not found"}), 404

# === ROUTE API HOMEPAGE ===

@app.route('/api', methods=['GET'])
def api_home():
    return jsonify({
        "message": "Weather API v2.0",
        "endpoints": {
            "weather": {
                "current": "/api/weather/current?city=Jakarta",
                "forecast": "/api/weather/forecast?city=Jakarta"
            },
            "wilayah": {
                "provinces": "/api/wilayah/provinces",
                "regencies": "/api/wilayah/regencies/<province_code>",
                "districts": "/api/wilayah/districts/<regency_code>",
                "villages": "/api/wilayah/villages/<district_code>"
            },
            "chatbot": {
                "ask": "/api/chat (POST)",
                "reset": "/api/chat/reset (POST)"
            },
            "favorites": {
                "list": "/api/favorites",
                "add": "/api/favorites (POST)",
                "delete": "/api/favorites/<city> (DELETE)"
            }
        },
        "status": {
            "gemini_ai": "available" if GEMINI_AVAILABLE else "not available"
        }
    }), 200

# === ROUTE CUACA ===

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather_route():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parameter city diperlukan"}), 400
    
    weather_data = api_service.get_current_weather(city)
    if "error" in weather_data:
        return jsonify(weather_data), 404
    return jsonify(weather_data), 200

@app.route('/api/weather/forecast', methods=['GET'])
def get_forecast_route():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parameter city diperlukan"}), 400
    
    forecast_data = api_service.get_5day_forecast(city)
    if isinstance(forecast_data, dict) and "error" in forecast_data:
        return jsonify(forecast_data), 404
    return jsonify(forecast_data), 200

# === ROUTE WILAYAH.ID ===

@app.route('/api/wilayah/provinces', methods=['GET'])
def get_provinces():
    data, status_code = api_service.get_wilayah_data("/provinces.json")
    return jsonify(data), status_code

@app.route('/api/wilayah/regencies/<province_code>', methods=['GET'])
def get_regencies(province_code):
    data, status_code = api_service.get_wilayah_data(f"/regencies/{province_code}.json")
    return jsonify(data), status_code

@app.route('/api/wilayah/districts/<regency_code>', methods=['GET'])
def get_districts(regency_code):
    data, status_code = api_service.get_wilayah_data(f"/districts/{regency_code}.json")
    return jsonify(data), status_code

@app.route('/api/wilayah/villages/<district_code>', methods=['GET'])
def get_villages(district_code):
    data, status_code = api_service.get_wilayah_data(f"/villages/{district_code}.json")
    return jsonify(data), status_code

# === ROUTE CHATBOT GEMINI AI ===

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    global chat_session  # Deklarasi global di AWAL fungsi
    
    if not GEMINI_AVAILABLE:
        return jsonify({"error": "Gemini AI tidak tersedia"}), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Pesan tidak boleh kosong"}), 400
        
        # Error handling yang lebih baik
        try:
            response = chat_session.send_message(user_message)
            response_text = response.text
        except Exception as gemini_error:
            print(f"Gemini API Error: {str(gemini_error)}")
            # Jika error, coba reinitialize chat session
            chat_session = model.start_chat(history=[
                {"role": "user", "parts": [SYSTEM_PROMPT]},
                {"role": "model", "parts": ["Baik, saya siap membantu!"]}
            ])
            response = chat_session.send_message(user_message)
            response_text = response.text
        
        return jsonify({
            "message": user_message,
            "response": response_text,
            "timestamp": data.get('timestamp')
        }), 200
        
    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        return jsonify({
            "error": "Maaf, terjadi kesalahan pada chatbot",
            "details": str(e)
        }), 500

@app.route('/api/chat/reset', methods=['POST'])
def reset_chat():
    global chat_session  # Deklarasi global di AWAL fungsi
    
    if not GEMINI_AVAILABLE:
        return jsonify({"error": "Gemini AI tidak tersedia"}), 503
    
    chat_session = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Baik, saya siap membantu!"]}
    ])
    return jsonify({"message": "Chat history telah direset"}), 200

# === ROUTE FAVORIT ===

@app.route('/api/favorites', methods=['GET'])
def get_favorites_route():
    favorites = data_manager.load_favorites()
    return jsonify(favorites), 200

@app.route('/api/favorites', methods=['POST'])
def add_favorite_route():
    data = request.get_json()
    city = data.get('city')
    
    if not city:
        return jsonify({"error": "Field city diperlukan"}), 400
    
    favorites = data_manager.load_favorites()
    if city not in favorites:
        favorites.append(city)
        data_manager.save_favorites(favorites)
        return jsonify({"message": f"{city} ditambahkan ke favorit"}), 201
    
    return jsonify({"message": f"{city} sudah ada di favorit"}), 200

@app.route('/api/favorites/<city>', methods=['DELETE'])
def delete_favorite_route(city):
    favorites = data_manager.load_favorites()
    if city in favorites:
        favorites.remove(city)
        data_manager.save_favorites(favorites)
        return jsonify({"message": f"{city} dihapus dari favorit"}), 200
    
    return jsonify({"error": "Kota tidak ditemukan di favorit"}), 404

# === HEALTH CHECK ===

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "OK", 
        "message": "Server berjalan normal",
        "gemini_ai": "available" if GEMINI_AVAILABLE else "not available"
    }), 200

# === MAIN ===

if __name__ == "__main__":
    print("=" * 60)
    print("WEATHER APP SERVER")
    print("=" * 60)
    print("URL: http://localhost:5000")
    print("Frontend: http://localhost:5000")
    print("API Docs: http://localhost:5000/api")
    print("\nFeatures:")
    print("  - Weather API (OpenWeatherMap)")
    print("  - Wilayah.id API (Prov -> Kab -> Kec -> Desa)")
    if GEMINI_AVAILABLE:
        print("  - Gemini AI Chatbot (Weather Topics)")
    else:
        print("  - Gemini AI Chatbot (Not Available)")
    print("  - Favorites Management")
    print("=" * 60)
    print("Tekan CTRL+C untuk stop server\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')